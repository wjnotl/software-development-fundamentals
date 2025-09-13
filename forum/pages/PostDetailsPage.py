import os
import customtkinter as ctk

from utils.core.Page import Page
import utils.core.Global as Global
from utils.ui.BackButton import BackButton
from utils.ui.DeleteButton import DeleteButton
from utils.ui.Message import ConfirmationMessage, ErrorMessage
from utils.processing.TextProcessing import time_ago_short
from utils.processing.ImageProcessing import circular_crop, prepare_post_image

from forum.ui.Header import Header
from forum.ui.LikeButton import LikeButton
from forum.ui.ReplyEntry import ReplyEntry
from forum.ui.MainComment import MainComment
from forum.controllers.PostController import PostController
from forum.controllers.ContentController import ContentController


class PostDetailsPage(Page):
    def __init__(self, parentFrame, id):
        super().__init__(parentFrame)
        self.id = id

    def load_data(self):
        """Load the post data from the controller."""

        self.content = PostController.get_post_public_data(
            Global.forumAccount["token"], self.id
        )
        
        if self.content is None:
            ErrorMessage("Post not found")
            return False

    def create_UI(self):
        """Create the header and the main content of the post page."""

        Header(self._frame)

        self.contentFrame = ctk.CTkScrollableFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        self.contentFrame.pack(fill="both", expand=True)

        # Back Button
        BackButton(self.contentFrame).pack(padx=10, pady=10, anchor="w")

        authorFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        authorFrame.pack(padx=(20, 10), pady=10, fill="x")

        # Author Profile Picture
        pfpPath = os.path.join(Global.CURRENT_PATH, "forum", "img", "pfp_gray.png")
        customPfpPath = (
            os.path.join(
                Global.CURRENT_PATH,
                "forum",
                "uploads",
                "pfp",
                f"{self.content["account"]["id"]}.png",
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

        # Author Name and Post Time
        postName = (
            self.content["account"]["name"]
            if self.content["account"]
            else "Deleted User"
        )
        postTime = time_ago_short(self.content["creationTime"])
        nameTimeLabel = ctk.CTkLabel(
            authorFrame,
            text=postName + " • " + postTime,
            text_color="black",
            font=("Segoe UI", 13),
            anchor="w",
        )
        nameTimeLabel.pack(side="left", padx=(5, 0))

        # Delete Post Button
        if (
            self.content["account"]
            and Global.forumAccount["id"] == self.content["account"]["id"]
        ):
            DeleteButton(
                authorFrame,
                callback=lambda: ConfirmationMessage(
                    "Are you sure you want to delete this post?",
                    callback=self.delete_post,
                ),
                tooltipText="Delete Post",
            ).pack(side="right", padx=(0, 10))

        # Post Title
        titleLabel = ctk.CTkLabel(
            self.contentFrame,
            text=self.content["title"],
            text_color="black",
            font=("Segoe UI", 16, "bold"),
            anchor="w",
            justify="left",
            wraplength=320,
        )
        titleLabel.pack(padx=20, pady=(0, 10), fill="x")

        # Post Image
        postImagePath = os.path.join(
            Global.CURRENT_PATH,
            "forum",
            "uploads",
            "post",
            f"{self.content["id"]}.png",
        )
        if os.path.exists(postImagePath):
            postImage = ctk.CTkLabel(
                self.contentFrame,
                text="",
                image=prepare_post_image(postImagePath, 324, 243),
            )
            postImage.pack(padx=20, pady=(0, 10), fill="x")

        # Post Content
        postContent = self.content["text"]
        if postContent:
            postContentLabel = ctk.CTkLabel(
                self.contentFrame,
                text=postContent,
                text_color="black",
                font=("Segoe UI", 13.5),
                anchor="w",
                justify="left",
                wraplength=320,
            )
            postContentLabel.pack(padx=20, pady=(0, 10), fill="x")

        # Post Action Frame
        self.actionFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        self.actionFrame.pack(anchor="w", padx=(10, 0))
        self.actionFrame.replyEntry = None

        # Post Likes
        LikeButton(self.actionFrame, self.content)

        # Join conversation
        ctk.CTkButton(
            self.actionFrame,
            text="Join Conversation",
            fg_color="#195a92",
            hover_color="#123f66",
            command=self.join_conversation,
            width=0,
        ).pack(anchor="w", side="left")

        # Comments Frame
        self.commentsFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        self.commentsFrame.pack(fill="x", padx=(20, 0), pady=20)
        self.commentsFrame.childs = []

        # Generate Comments
        mainComments = ContentController.get_replies(
            self.content["id"], Global.forumAccount["token"]
        )
        mainComments.reverse()
        for comment in mainComments:
            ele = MainComment(self.commentsFrame, comment)
            ele.pack(pady=(0, 20), fill="x")
            self.commentsFrame.childs.append(ele)

    def delete_post(self):
        """Process deleting the post"""

        error = PostController.delete(Global.forumAccount["token"], self.content["id"])
        if isinstance(error, str):
            ErrorMessage(error)
            return

        Global.pageManagers["forum"].back()

    def join_conversation(self):
        """Show a new entry to write comments"""

        if (
            self.actionFrame.replyEntry is None
            or not self.actionFrame.replyEntry.winfo_exists()
        ):
            replyEntry = ReplyEntry(
                self.contentFrame, self.content, self.commentsFrame, True
            )
            replyEntry.pack(after=self.actionFrame, fill="x", padx=20, pady=10)
            self.actionFrame.replyEntry = replyEntry
