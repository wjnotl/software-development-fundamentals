import os
import customtkinter as ctk

import utils.core.Global as Global
from utils.ui.DeleteButton import DeleteButton
from utils.ui.Message import ConfirmationMessage, ErrorMessage
from utils.processing.TextProcessing import time_ago_short
from utils.processing.ImageProcessing import circular_crop

from forum.ui.LikeButton import LikeButton
from forum.controllers.ReplyController import ReplyController


class Comment(ctk.CTkFrame):
    """A UI widget representing a forum comment."""

    def __init__(self, master, content, mainComment=False, deleteCallback=lambda: None):
        """Initialize the Comment widget.
        :param master: Parent widget (container for this frame).
        :param content: Dictionary containing comment data.
        :param mainComment: Whether this comment is the main post (affects layout).
        :param deleteCallback: Callable to execute after a comment is successfully deleted.
        """

        super().__init__(master, fg_color="transparent", corner_radius=0)

        self.master = master
        self.content = content
        self.mainComment = mainComment
        self.deleteCallback = deleteCallback

        authorFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        authorFrame.pack(padx=(0, 10), fill="x")

        # Author Profile Picture
        pfpPath = os.path.join(Global.CURRENT_PATH, "forum", "img", "pfp_gray.png")
        customPfpPath = (
            (
                os.path.join(
                    Global.CURRENT_PATH,
                    "forum",
                    "uploads",
                    "pfp",
                    f"{self.content["account"]["id"]}.png",
                )
            )
            if self.content["account"]
            else pfpPath
        )
        pfp = circular_crop(
            customPfpPath if os.path.exists(customPfpPath) else pfpPath,
            30,
            30,
        )
        pfpImage = ctk.CTkLabel(
            authorFrame,
            text="",
            image=pfp,
            width=30,
            height=30,
        )
        pfpImage.pack(side="left")

        # Author Name and Comment Time
        authorName = (
            self.content["account"]["name"]
            if self.content["account"]
            else "Deleted User"
        )
        postTime = time_ago_short(self.content["creationTime"])
        nameTimeLabel = ctk.CTkLabel(
            authorFrame,
            text=authorName + " • " + postTime,
            text_color="black",
            font=("Segoe UI", 13),
            anchor="w",
        )
        nameTimeLabel.pack(side="left", padx=(5, 0))

        # Delete Comment Button
        if (
            self.content["account"]
            and Global.forumAccount["id"] == self.content["account"]["id"]
        ):
            DeleteButton(
                authorFrame,
                callback=lambda: ConfirmationMessage(
                    "Are you sure you want to delete this comment?",
                    callback=self.delete_comment,
                ),
                tooltipText="Delete Comment",
            ).pack(side="right", padx=(0, 10))

        # Comment Container
        self.commentContainer = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.commentContainer.pack(fill="x", padx=(25, 0))

        # Content
        contentLabel = ctk.CTkLabel(
            self.commentContainer,
            text=self.content["text"],
            text_color="black",
            font=("Segoe UI", 13.5),
            anchor="w",
            justify="left",
            wraplength=285 if self.mainComment else 245,
        )
        contentLabel.pack(fill="x", padx=(10, 0))

        # Action Frame
        self.actionFrame = ctk.CTkFrame(
            self.commentContainer, corner_radius=0, fg_color="transparent"
        )
        self.actionFrame.pack(anchor="w", pady=(5, 0))
        self.actionFrame.replyEntry = None

        # Like
        LikeButton(self.actionFrame, self.content)

    def delete_comment(self):
        """Delete this comment from the forum.
        Sends a deletion request via `ReplyController`. If successful,
        removes the widget from the UI and triggers the `deleteCallback`.
        """

        # Send deletion request
        returnValue = ReplyController.delete(
            Global.forumAccount["token"], self.content["id"]
        )
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        # Remove sub reply if any
        if self.mainComment:
            for ele in self.master.childs:
                if ele == self:
                    self.master.childs.remove(ele)
                    break

        # Destroy widget
        self.destroy()
        self.deleteCallback()
