import customtkinter as ctk

import utils.core.Global as Global
from utils.ui.Tooltip import Tooltip

from forum.ui.Comment import Comment
from forum.ui.ReplyEntry import ReplyEntry
from forum.controllers.ContentController import ContentController


class MainComment(Comment):
    """A specialized Comment widget that represents a top-level comment.
    Adds support for:
    - Replying with a `ReplyEntry`
    - Expanding/collapsing nested sub-comments
    - Displaying the number of replies
    """

    def __init__(self, master, content):
        """Initialize the main comment widget.
        :param master: Parent container for this comment.
        :param content: Dictionary with comment data.
        """

        super().__init__(master, content, mainComment=True)

        self.content = content

        # Reply
        ctk.CTkButton(
            self.actionFrame,
            text="Reply",
            fg_color="#195a92",
            hover_color="#123f66",
            command=self.add_comment,
            width=0,
        ).pack(anchor="w", side="left")

        # Expand button
        self.expandMore = False
        self.expandButton = ctk.CTkButton(
            self.commentContainer,
            text="",
            text_color="#065fd4",
            fg_color="transparent",
            hover_color="#ebebeb",
            command=self.expand,
            width=20,
            height=20,
        )

        # Sub Comments Container
        self.subCommentContainer = ctk.CTkFrame(
            self.commentContainer, corner_radius=0, fg_color="transparent"
        )

        # Generate sub comments
        for comment in ContentController.get_replies(
            self.content["id"], Global.forumAccount["token"]
        ):
            Comment(
                self.subCommentContainer,
                comment,
                deleteCallback=self.update_sub_comment_container,
            ).pack(fill="x", pady=(0, 10))
        self.update_sub_comment_container()

        # Expand button tooltip
        self.expandButtonTooltip = Tooltip(self.expandButton, "Show more")

    def add_comment(self):
        """Insert a reply entry field below the main comment.
        Creates a `ReplyEntry` widget if one is not already present 
        in this comment's action frame.
        """

        if (
            self.actionFrame.replyEntry is None
            or not self.actionFrame.replyEntry.winfo_exists()
        ):
            replyEntry = ReplyEntry(
                self.commentContainer,
                self.content,
                self.subCommentContainer,
                False,
                self.update_sub_comment_container,
            )
            replyEntry.pack(after=self.actionFrame, padx=(10, 20), pady=10, fill="x")
            self.actionFrame.replyEntry = replyEntry

    def update_sub_comment_container(self):
        """Refresh the sub-comments container.
        - If there are no replies: hides the expand button and container.
        - If replies exist: shows the expand button with the reply count 
          and updates its icon (expand/collapse state).
        """

        replyCount = len(self.subCommentContainer.winfo_children())

        if replyCount < 1:
            # No sub comments
            self.expandMore = False
            self.expandButton.pack_forget()
            self.subCommentContainer.pack_forget()
            return

        # Expand button
        self.expandButton.pack(anchor="w")
        self.expandButton.configure(
            image=(
                Global.get_ctk_cache_image("forum", "expand_up.png", (20, 20))
                if self.expandMore
                else Global.get_ctk_cache_image("forum", "expand_down.png", (20, 20))
            ),
            text=str(replyCount) + (" replies" if replyCount > 1 else " reply"),
        )

    def expand(self):
        """Toggle between showing and hiding sub-comments.
        Updates the expand button icon and tooltip accordingly.
        """

        self.expandMore = not self.expandMore  # Toggle

        self.expandButton.configure(
            image=(
                Global.get_ctk_cache_image("forum", "expand_up.png", (20, 20))
                if self.expandMore
                else Global.get_ctk_cache_image("forum", "expand_down.png", (20, 20))
            )
        )

        if self.expandMore:
            self.subCommentContainer.pack(fill="x", padx=(10, 0))
            self.expandButtonTooltip.hide_tooltip()
            self.expandButtonTooltip.text = "Show less"
        else:
            self.subCommentContainer.pack_forget()
            self.expandButtonTooltip.hide_tooltip()
            self.expandButtonTooltip.text = "Show more"
