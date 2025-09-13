import os
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog

import utils.core.Global as Global
from utils.core.Page import Page
from utils.ui.BackButton import BackButton
from utils.ui.SaveButton import SaveButton
from utils.ui.Message import ConfirmationMessage, ErrorMessage
from utils.processing.ImageProcessing import circular_crop
from utils.processing.StorageProcessing import save_forum_account_token

from forum.ui.Header import Header
from forum.controllers.AccountController import AccountController


class AccountPage(Page):
    def create_UI(self):
        """Create the header and the main content of account page."""

        Header(self._frame)

        contentFrame = ctk.CTkFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        contentFrame.pack(fill="both", expand=True)
        contentFrame.pack_propagate(False)

        # Back Button
        BackButton(contentFrame, self.is_changed).pack(padx=10, pady=10, anchor="w")

        # Account
        accountLabel = ctk.CTkLabel(
            contentFrame,
            text="Account",
            text_color="black",
            font=("Segoe UI", 20, "bold"),
            anchor="w",
        )
        accountLabel.pack(padx=20, pady=10, fill="x")

        # Name
        self.oriName = Global.forumAccount["name"]
        ctk.CTkLabel(
            contentFrame,
            text="Name",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(anchor="w", padx=20)

        self.nameEntry = ctk.CTkEntry(
            contentFrame, placeholder_text="Enter your displayable name"
        )
        self.nameEntry.insert(0, self.oriName)
        self.nameEntry.pack(anchor="w", padx=20, pady=(0, 20), fill="x")

        # Profile Picture
        ctk.CTkLabel(
            contentFrame,
            text="Profile Picture",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(padx=20)

        pfpPath = os.path.join(
            Global.CURRENT_PATH,
            "forum",
            "uploads",
            "pfp",
            f"{Global.forumAccount["id"]}.png",
        )
        self.oriImagePath = pfpPath if os.path.exists(pfpPath) else None
        self.changePfp = False

        self.pfpContainer = ctk.CTkLabel(
            contentFrame,
            text="",
            image=circular_crop(
                self.oriImagePath
                or os.path.join(Global.CURRENT_PATH, "forum", "img", "pfp_gray.png"),
                150,
                150,
            ),
            width=150,
            height=150,
            fg_color="transparent",
        )
        self.pfpContainer.pack(padx=20)
        self.pfpContainer.image = None

        pfpButtonFrame = ctk.CTkFrame(
            contentFrame, corner_radius=0, fg_color="transparent"
        )
        pfpButtonFrame.pack(padx=20, pady=(10, 60))

        ctk.CTkButton(
            pfpButtonFrame,
            text="Upload",
            command=self.upload_pfp,
            width=0,
        ).pack(padx=5, anchor="e", side="left", ipady=2)

        ctk.CTkButton(
            pfpButtonFrame,
            text="Remove",
            command=self.remove_pfp,
            fg_color="red1",
            hover_color="red3",
            width=0,
        ).pack(padx=5, anchor="w", side="right", ipady=2)

        # Save Changes Button
        self.saveChangesButton = SaveButton(contentFrame, self.save_changes, self.is_changed)
        self.saveChangesButton.pack(padx=20, pady=(0, 10), anchor="w", ipady=2)

        # Delete Account Button
        self.deleteAccountButton = ctk.CTkButton(
            contentFrame,
            text="Delete Account",
            fg_color="red1",
            hover_color="red3",
            text_color="white",
            command=lambda: ConfirmationMessage(
                "Are you sure you want to delete your account?",
                callback=self.delete_account,
            ),
            width=0,
        )
        self.deleteAccountButton.pack(padx=20, pady=(0, 10), anchor="w", ipady=2)

        # Logout Button
        self.logoutButton = ctk.CTkButton(
            contentFrame,
            text="Logout",
            fg_color="red1",
            hover_color="red3",
            text_color="white",
            command=lambda: ConfirmationMessage(
                "Are you sure you want to log out?",
                callback=self.logout,
            ),
            width=0,
        )
        self.logoutButton.pack(padx=20, pady=(0, 10), anchor="w", ipady=2)

        # Trigger event when typing
        self.nameEntry.bind("<KeyRelease>", lambda event: self.saveChangesButton.update_state())

    def upload_pfp(self):
        """Open file explorer for user to select an image file.
        If selected, crop it into circle shape and set it as profile picture.
        Only accept .png, .jpg, .jpeg, and .bmp format.
        """

        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            try:
                pil_image = Image.open(file_path)
                ctk_image = ctk.CTkImage(pil_image, size=(150, 150))

                self.pfpContainer.configure(image=circular_crop(file_path, 150, 150))
                self.pfpContainer.image = (
                    ctk_image  # Keep a reference to prevent garbage collection
                )

                self.changePfp = True
                self.saveChangesButton.update_state()
            except Exception as e:
                print(f"Error loading image: {e}")

    def remove_pfp(self):
        """Reset profile picture to default gray one."""

        self.pfpContainer.configure(
            image=circular_crop(
                os.path.join(Global.CURRENT_PATH, "forum", "img", "pfp_gray.png"),
                150,
                150,
            )
        )

        self.changePfp = self.oriImagePath != None
        self.saveChangesButton.update_state()

    def is_changed(self):
        """Check whether any changes have been made in account page."""
        return self.oriName != self.nameEntry.get() or self.changePfp

    def save_changes(self):
        """Update account information."""
        name = self.nameEntry.get()

        returnValue = AccountController.edit_profile(
            Global.forumAccount["token"], name, self.pfpContainer.image, self.changePfp
        )
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.forumAccount = returnValue
        Global.pageManagers["forum"].currentPage.refresh_frame()

    def delete_account(self):
        """Delete current account."""

        from forum.pages.LoginPage import LoginPage

        error = AccountController.delete_account(Global.forumAccount["token"])
        if error:
            ErrorMessage(error)

        Global.forumAccount = None
        save_forum_account_token("")
        Global.pageManagers["forum"].clear_history()
        Global.pageManagers["forum"].show_page(LoginPage)

    def logout(self):
        """Log out current account by deleting token and redirect to login page."""

        from forum.pages.LoginPage import LoginPage

        error = AccountController.process_logout(Global.forumAccount["token"])
        if error:
            ErrorMessage(error)
            
        save_forum_account_token("")
        Global.forumAccount = None
        Global.pageManagers["forum"].show_page(LoginPage)
