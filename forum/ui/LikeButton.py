import customtkinter as ctk

import utils.core.Global as Global
from utils.ui.Message import ErrorMessage
from utils.processing.TextProcessing import format_number_short

from forum.controllers.ContentController import ContentController


class LikeButton:
    """A UI widget that represents a like button with a counter.
    Displays a thumb icon that toggles between "liked" and "not liked" states.
    Updates the like count and triggers a callback when clicked.
    """

    def __init__(self, master, content, hoverColor="#ebebeb", callback=lambda content: None):
        """Initialize the LikeButton widget.
        :param master: Parent widget where the like button will be placed.
        :param content: Dictionary containing like data.
        :param hoverColor: Background color when hovering over the button.
        :param callback: Callable executed after the like state is toggled.
        """

        self.master = master
        self.content = content
        self.hoverColor = hoverColor
        self.callback = callback

        self.isLiked = False

        # Like frame
        self.likeFrame = ctk.CTkFrame(
            self.master,
            corner_radius=0,
            fg_color="transparent",
        )
        self.likeFrame.pack(side="left", padx=10)

        # Like button
        self.likeButton = ctk.CTkLabel(
            self.likeFrame,
            text="",
            fg_color="transparent",
            cursor="hand2",
            width=20,
            height=20,
        )
        self.likeButton.pack(side="left", padx=(0, 5))

        # Like count
        self.likeCountLabel = ctk.CTkLabel(
            self.likeFrame,
            text="",
            text_color="#666666",
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        )
        self.likeCountLabel.pack(side="left")

        self.update_like_display()

        # Hover like button effect
        self.likeButton.bind("<Enter>", lambda event: self.hover_like())
        self.likeButton.bind("<Leave>", lambda event: self.unhover_like())

        # Click like button
        self.likeButton.bind("<Button-1>", lambda event: self.like_button_click())

    def update_like_display(self):
        """Refresh the button display.
        Updates the thumb icon (filled or empty) based on `isLiked` 
        and sets the displayed like count.
        """

        self.isLiked = self.content["isLiked"]

        self.likeButton.configure(
            image=(
                Global.get_ctk_cache_image("forum", "thumb_up.png", (20, 20))
                if self.isLiked
                else Global.get_ctk_cache_image("forum", "thumb_up_empty.png", (20, 20))
            )
        )
        self.likeCountLabel.configure(
            text=format_number_short(self.content["likesCount"])
        )

    def hover_like(self):
        """Handle hover event.
        Updates the thumb icon to its hover version depending 
        on whether the post is liked.
        """

        self.likeButton.configure(
            image=(
                Global.get_ctk_cache_image("forum", "thumb_up_hover.png", (20, 20))
                if self.isLiked
                else Global.get_ctk_cache_image(
                    "forum", "thumb_up_empty_hover.png", (20, 20)
                )
            )
        )

    def unhover_like(self):
        """Handle mouse leave event.
        Restores the thumb icon to the normal state.
        """

        self.likeButton.configure(
            image=(
                Global.get_ctk_cache_image("forum", "thumb_up.png", (20, 20))
                if self.isLiked
                else Global.get_ctk_cache_image("forum", "thumb_up_empty.png", (20, 20))
            )
        )

    def like_button_click(self):
        """Handle click event.
        Toggles the like state via `ContentController.toggle_like`. 
        Updates the content and display if successful, or shows an 
        error message on failure.
        """

        returnValue = ContentController.toggle_like(
            Global.forumAccount["token"], self.content["id"]
        )
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        self.content = returnValue
        self.callback(returnValue)
        self.update_like_display()
