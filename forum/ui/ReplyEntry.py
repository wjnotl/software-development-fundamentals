import customtkinter as ctk

import utils.core.Global as Global
from utils.ui.Message import ErrorMessage

from forum.controllers.ReplyController import ReplyController


class ReplyEntry(ctk.CTkFrame):
    """A UI frame for entering and submitting a reply to a comment or content item.
    This frame provides a textbox for typing a reply and two buttons:
    - "Comment" to submit the reply
    - "Cancel" to close the reply entry without posting
    The reply is sent through `ReplyController.create` and dynamically inserted
    into the comment frame either as a `MainComment` or a normal `Comment`.
    """

    def __init__(
        self, contentFrame, content, commentFrame, mainComment, callback=lambda: None
    ):
        """Initialize the reply entry frame.
        :param contentFrame: The parent frame where this reply entry is placed.
        :param content: A dictionary containing content information.
        :param commentFrame: The frame where the new comment will be inserted.
        :param mainComment: Boolean indicating if the reply is a main comment.
        :param callback: Function to call after a reply is successfully posted.
        """

        super().__init__(
            contentFrame,
            fg_color="white",
            bg_color="transparent",
            corner_radius=6,
            border_width=2,
        )

        self.content = content
        self.contentFrame = contentFrame
        self.commentFrame = commentFrame
        self.mainComment = mainComment
        self.callback = callback

        self.textBox = ctk.CTkTextbox(
            self,
            fg_color="transparent",
            wrap="word",
            border_spacing=0,
            border_width=0,
            corner_radius=0,
            height=70,
        )
        self.textBox.pack(fill="x", padx=(5, 10), pady=(5, 0))

        buttonFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        buttonFrame.pack(fill="x", padx=10, pady=(5, 10))

        self.totalCharLabel = ctk.CTkLabel(buttonFrame, text="0/1000", font=("Arial", 10), text_color="gray")
        self.totalCharLabel.pack(side="left")
        self.textBox.bind("<KeyRelease>", lambda _: self.update_total_char_label())

        ctk.CTkButton(
            buttonFrame,
            text="Comment",
            fg_color="#195a92",
            hover_color="#123f66",
            command=self.comment,
            width=0,
        ).pack(side="right", ipady=2)

        ctk.CTkButton(
            buttonFrame,
            text="Cancel",
            fg_color="red1",
            hover_color="red3",
            command=self.cancel,
            width=0,
        ).pack(side="right", ipady=2, padx=10)

    def comment(self):
        """Handle the comment submission.
        Retrieves the text from the textbox.
        Sends the reply via `ReplyController.create`.
        On success:
        -   If `mainComment` is True, inserts as a `MainComment`.
        -   Otherwise, inserts as a `Comment` and calls the callback.
        On failure, shows an error message.
        Destroys the reply entry after posting.
        """

        from forum.ui.Comment import Comment
        from forum.ui.MainComment import MainComment

        text = self.textBox.get("0.0", "end").strip()

        # Send create request
        returnValue = ReplyController.create(Global.forumAccount["token"], text, self.content["id"])
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        # Insert comment to frame
        if self.mainComment:
            comment = MainComment(self.commentFrame, returnValue)
            if self.commentFrame.childs:
                comment.pack(before=self.commentFrame.childs[0], pady=(0, 20), fill="x")
            else:
                comment.pack(pady=(0, 20), fill="x")
            self.commentFrame.childs.insert(0, comment)
        else:
            Comment(self.commentFrame, returnValue, deleteCallback=self.callback).pack(
                pady=(0, 20), fill="x"
            )
            self.callback()

        # Destroy reply input
        self.destroy()

    def update_total_char_label(self):
        """Update the total character label with current length of text in the textbox."""

        textLength = len(self.textBox.get("0.0", "end").strip())
        self.totalCharLabel.configure(text=f"{textLength}/1000")

        if textLength > 1000:
            self.totalCharLabel.configure(text_color="red")
        else:
            self.totalCharLabel.configure(text_color="gray")

    def cancel(self):
        """Cancel the reply entry and remove the frame from the UI."""
        
        self.destroy()
