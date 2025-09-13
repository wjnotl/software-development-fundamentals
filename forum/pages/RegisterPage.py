import customtkinter as ctk

from utils.core.Page import Page
import utils.core.Global as Global
from utils.ui.Message import ErrorMessage
from utils.processing.StorageProcessing import save_forum_account_token

from forum.ui.PasswordEntry import PasswordEntry
from forum.pages.HomePage import HomePage
from forum.controllers.AccountController import AccountController


class RegisterPage(Page):
    def create_UI(self):
        """Create the header and the main content of the register account page."""

        formFrame = ctk.CTkFrame(
            self._frame,
            corner_radius=7,
            fg_color="#ffffff",
            border_width=1,
            border_color="#666666",
        )
        formFrame.pack(expand=True)

        # Title
        titleLabel = ctk.CTkLabel(
            formFrame,
            text="Register",
            text_color="black",
            font=("Segoe UI", 20, "bold"),
        )
        titleLabel.pack(anchor="w", padx=20, pady=20)

        # Username
        ctk.CTkLabel(
            formFrame,
            text="Username",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(anchor="w", padx=20)

        self.usernameEntry = ctk.CTkEntry(
            formFrame, placeholder_text="Enter your username", width=200
        )
        self.usernameEntry.pack(anchor="w", padx=20)

        # Password
        ctk.CTkLabel(
            formFrame,
            text="Password",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(anchor="w", padx=20, pady=(20, 0))

        self.passwordEntry = PasswordEntry(
            formFrame, placeholder_text="Enter your password", width=200
        )
        self.passwordEntry.pack(padx=20)

        # Confirm Password
        ctk.CTkLabel(
            formFrame,
            text="Confirm Password",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(anchor="w", padx=20, pady=(20, 0))

        self.confirmPasswordEntry = PasswordEntry(
            formFrame, placeholder_text="Enter your password again", width=200
        )
        self.confirmPasswordEntry.pack(padx=20)

        # Register Button
        ctk.CTkButton(
            formFrame,
            text="Register",
            fg_color="#195a92",
            border_color="#195a92",
            text_color="white",
            font=("Segoe UI", 14, "bold"),
            command=self.register,
            width=80,
            height=30,
            anchor="n",
        ).pack(anchor="w", padx=20, pady=(30, 0))

        # Login Redirection
        ctk.CTkLabel(
            formFrame,
            text="Have an account?",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(padx=(20, 0), pady=(0, 20), side="left")
        haveAccountButton = ctk.CTkButton(
            formFrame,
            text="Login",
            fg_color="white",
            border_color="white",
            hover_color="white",
            text_color="#195a92",
            font=("Segoe UI", 14, "bold"),
            command=self.login,
            width=0,
        )
        haveAccountButton.pack(side="left", pady=(0, 20))

        # Hover Login Effect
        haveAccountButton.bind(
            "<Enter>",
            lambda event: haveAccountButton.configure(
                font=("Segoe UI", 14, "bold", "underline")
            ),
        )
        haveAccountButton.bind(
            "<Leave>",
            lambda event: haveAccountButton.configure(font=("Segoe UI", 14, "bold")),
        )

    def login(self):
        """Redirect to the login page."""

        from forum.pages.LoginPage import LoginPage

        Global.pageManagers["forum"].back()
        Global.pageManagers["forum"].show_page(LoginPage)

    def register(self):
        """Process the registration request."""

        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        confirmPassword = self.confirmPasswordEntry.get()

        returnValue = AccountController.create_account(
            username, password, confirmPassword
        )
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.forumAccount = returnValue
        save_forum_account_token(returnValue["token"])
        Global.pageManagers["forum"].show_page(HomePage, "")
