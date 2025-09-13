import customtkinter as ctk

from utils.core.Page import Page
import utils.core.Global as Global

from forum.ui.Header import Header
from forum.ui.HomePostContainer import HomePostContainer
from forum.controllers.PostController import PostController


class HomePage(Page):
    def __init__(self, parentFrame, keyword=""):
        super().__init__(parentFrame)
        self.keyword = keyword

    def load_data(self):
        """Get posts data from the controller."""

        self.posts = PostController.get_home_posts(
            Global.forumAccount["token"], self.keyword
        )

    def create_UI(self):
        """Create the header and the main content of the home page."""

        Header(self._frame, self.keyword)

        contentFrame = ctk.CTkScrollableFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        contentFrame.pack(fill="both", expand=True)

        first = True
        for post in self.posts:
            HomePostContainer(contentFrame, post, first)
            first = False

        if len(self.posts) == 0:
            ctk.CTkLabel(
                contentFrame,
                text="No posts found",
                text_color="#666666",
            ).pack(padx=20, pady=20, expand=True)
