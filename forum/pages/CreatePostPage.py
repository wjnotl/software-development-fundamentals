from PIL import Image
import customtkinter as ctk
from tkinter import filedialog

from utils.core.Page import Page
import utils.core.Global as Global
from utils.ui.Message import ErrorMessage
from utils.ui.BackButton import BackButton
from utils.processing.ImageProcessing import prepare_post_image

from forum.ui.Header import Header
from forum.controllers.PostController import PostController


class CreatePostPage(Page):
    def create_UI(self):
        """Create the header and the main content of create new post page."""

        Header(self._frame)

        self.contentFrame = ctk.CTkScrollableFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        self.contentFrame.pack(fill="both", expand=True)

        # Back Button
        BackButton(self.contentFrame, self.is_changed).pack(padx=10, pady=10, anchor="w")

        # Create Post
        createPostLabel = ctk.CTkLabel(
            self.contentFrame,
            text="Create Post",
            text_color="black",
            font=("Segoe UI", 20, "bold"),
            anchor="w",
        )
        createPostLabel.pack(padx=20, pady=10, anchor="w")

        # Title
        ctk.CTkLabel(
            self.contentFrame,
            text="Title*",
            text_color="red",
            font=("Segoe UI", 15, "normal", "underline"),
        ).pack(anchor="w", padx=20)

        self.titleEntry = ctk.CTkEntry(
            self.contentFrame, placeholder_text="Enter post title"
        )
        self.titleEntry.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

        # Content
        ctk.CTkLabel(
            self.contentFrame,
            text="Content*",
            text_color="red",
            font=("Segoe UI", 15, "normal", "underline"),
        ).pack(anchor="w", padx=20)

        self.contentTextBox = ctk.CTkTextbox(
            self.contentFrame,
            height=200,
            border_width=2,
            fg_color="#F9F9FA",
            wrap="word"
        )
        self.contentTextBox.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

        # Image
        self.imageLabel = ctk.CTkLabel(
            self.contentFrame,
            text="Image",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        )
        self.imageLabel.pack(anchor="w", padx=20)

        self.imageContainer = None
        self.currentImage = None

        buttonsFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        buttonsFrame.pack(fill="x", padx=20, pady=(0, 25))

        # Upload Image button
        ctk.CTkButton(
            buttonsFrame, text="Upload", command=self.upload_image, width=0
        ).pack(anchor="w", side="left", ipady=2)

        # Remove Image button
        ctk.CTkButton(
            buttonsFrame,
            text="Remove",
            command=self.remove_image,
            fg_color="red1",
            hover_color="red3",
            width=0,
        ).pack(padx=10, anchor="w", side="left", ipady=2)

        # Create Post Button Button
        ctk.CTkButton(
            self.contentFrame,
            text="Create Post",
            fg_color="#195a92",
            hover_color="#123f66",
            width=0,
            command=self.create_post,
        ).pack(padx=20, anchor="w", ipady=2, ipadx=3, pady=(0, 30))

    def upload_image(self):
        """Open file explorer to select an image for the post.
        If selected successfully, display it in the container.
        If failed, show error message.
        Only allow png, jpg, jpeg, bmp format images.
        """

        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            try:
                if self.imageContainer:
                    self.imageContainer.destroy()

                self.imageContainer = ctk.CTkLabel(
                    self.contentFrame,
                    text="",
                    image=prepare_post_image(file_path, 324, 243),
                )
                self.imageContainer.pack(after=self.imageLabel, padx=20, pady=(0, 5))

                # Keep a reference to prevent garbage collection
                image = Image.open(file_path)
                self.currentImage = ctk.CTkImage(image, size=image.size)

            except Exception as e:
                print(f"Error loading image: {e}")

    def remove_image(self):
        if self.imageContainer:
            self.imageContainer.destroy()

        self.imageContainer = None
        self.currentImage = None

    def create_post(self):
        title = self.titleEntry.get()
        content = self.contentTextBox.get("1.0", "end-1c")
        image = self.currentImage

        from forum.pages.HomePage import HomePage

        returnValue = PostController.create(
            Global.forumAccount["token"], title, content, image
        )
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.pageManagers["forum"].clear_history()
        Global.pageManagers["forum"].show_page(HomePage, "")

    def is_changed(self):
        return (
            self.titleEntry.get() != ""
            or self.contentTextBox.get("1.0", "end-1c") != ""
            or self.currentImage is not None
        )
