import os
import customtkinter as ctk

import utils.core.Global as Global
from utils.processing.ImageProcessing import prepare_post_image
from utils.processing.TextProcessing import wrap_text_to_string, time_ago_short

from forum.ui.LikeButton import LikeButton


class HomePostContainer:
    """A UI widget representing a post preview on the forum home page.
    Displays the post's title, text or image preview, like button, and
    creation time. Supports hover effects and clicking to open the full post.
    """

    def __init__(self, frame, content, first=False):
        """Initialize a HomePostContainer widget.
        :param frame: Parent widget where this post container will be placed.
        :param content: Dictionary containing post data.
        :param first: If True, adds extra top padding (for the first post in a list).
        """

        self.content = content

        # Container
        self.container = ctk.CTkFrame(
            frame,
            corner_radius=7,
            fg_color="#ffffff",
            border_width=1,
            border_color="#d1d5db",
            cursor="hand2",
        )
        if first:
            self.container.pack(fill="x", padx=10, pady=10)
        else:
            self.container.pack(fill="x", padx=10, pady=(0, 10))

        # Title
        titleFont = ctk.CTkFont("Segoe UI", 15, "bold")
        titleLabel = ctk.CTkLabel(
            self.container,
            text="",
            text_color="black",
            font=titleFont,
            anchor="w",
            justify="left",
        )
        titleLabel.pack(anchor="w", padx=10, pady=(10, 5), fill="x", expand=True)
        titleLabel.configure(
            text=wrap_text_to_string(self.content["title"], titleFont, 320, 2)
        )

        imageLabel = None
        contentLabel = None
        imagePath = os.path.join(
            Global.CURRENT_PATH,
            "forum",
            "uploads",
            "post",
            f"{self.content["id"]}.png",
        )
        if os.path.exists(imagePath):
            # Image
            imageLabel = ctk.CTkLabel(
                self.container, text="", image=prepare_post_image(imagePath, 324, 243)
            )
            imageLabel.pack(anchor="w", padx=10, pady=(0, 10))
        else:
            # Text Content
            contentFont = ctk.CTkFont("Segoe UI", 12, "normal")
            contentLabel = ctk.CTkLabel(
                self.container,
                text="",
                text_color="#666666",
                font=contentFont,
                anchor="w",
                justify="left",
            )
            contentLabel.pack(anchor="w", padx=10, pady=(0, 10), fill="x", expand=True)
            contentLabel.configure(
                text=wrap_text_to_string(self.content["text"], contentFont, 320, 5)
            )

        postDataFrame = ctk.CTkFrame(
            self.container, corner_radius=0, fg_color="transparent"
        )
        postDataFrame.pack(anchor="w", pady=(0, 10), fill="x", padx=2)

        # Like
        self.likeButton = LikeButton(
            postDataFrame,
            self.content,
            "white",
            callback=self.like_button_click_callback,
        )

        # Time
        timeLabel = ctk.CTkLabel(
            postDataFrame,
            text=time_ago_short(self.content["creationTime"]),
            text_color="#666666",
            font=("Segoe UI", 13, "bold"),
        )
        timeLabel.pack(side="right", anchor="e", padx=10)

        # Hover container effect
        self.container.bind("<Enter>", lambda event: self.hover_container())
        self.container.bind("<Leave>", lambda event: self.unhover_container())

        # Click container effect
        for widget in [
            self.container,
            titleLabel,
            imageLabel,
            contentLabel,
            postDataFrame,
            self.likeButton.likeFrame,
            self.likeButton.likeCountLabel,
            timeLabel,
        ]:
            if widget:
                widget.bind("<Button-1>", lambda event: self.enter_post())

    def hover_container(self):
        """Handle hover event.
        Changes background color of the container when mouse enters.
        """

        self.container.configure(fg_color="#f7f7f7")

    def unhover_container(self):
        """Handle mouse leave event.
        Calls `check_mouse_leave` after a short delay to verify the 
        mouse has actually left the container.
        """

        self.container.after(100, self.check_mouse_leave)

    def check_mouse_leave(self):
        """Verify whether the mouse has left the container.
        If the mouse is no longer inside the container or its children,
        reset the background color.
        """

        widget_under_mouse = self.container.winfo_containing(
            self.container.winfo_pointerx(), self.container.winfo_pointery()
        )

        # Check if it's still inside self.container (or a child)
        parent = widget_under_mouse
        while parent is not None:
            if parent == self.container:
                return  # Still inside, do nothing
            parent = parent.master

        # Not inside anymore
        self.container.configure(fg_color="white")

    def like_button_click_callback(self, content):
        """Update container state when the like button is clicked.
        :param content: Updated post content data.
        """

        self.content = content

    def enter_post(self):
        """Navigate to the PostDetailsPage.
        Opens the detailed post view for the current post.
        """

        from forum.pages.PostDetailsPage import PostDetailsPage

        Global.pageManagers["forum"].show_page(PostDetailsPage, self.content["id"])
