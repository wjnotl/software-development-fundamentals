import os
import customtkinter as ctk

import utils.core.Global as Global
from utils.ui.Tooltip import Tooltip
from utils.processing.ImageProcessing import circular_crop


class Header:
    """A UI header widget for the forum.
    Provides a search bar, a "create post" button, and an account button
    with a profile picture. Each button navigates to the appropriate page.
    """

    def __init__(self, parentFrame, keyword=""):
        """Initialize the Header widget.
        :param parentFrame: Parent widget where the header is placed.
        :param keyword: Optional default text for the search input field.
        """

        headerFrame = ctk.CTkFrame(
            parentFrame,
            fg_color="#195a92",
            corner_radius=0,
        )
        headerFrame.pack(fill="x", ipady=10)

        # Search input
        self.searchInput = ctk.CTkEntry(headerFrame, placeholder_text="Search...")
        self.searchInput.pack(side="left", expand=True, fill="x", padx=(10, 0))

        # Set default keyword
        if keyword:
            self.searchInput.insert(0, keyword)

        searchButton = ctk.CTkButton(
            headerFrame,
            text="",
            fg_color="transparent",
            hover_color="#195a92",
            command=self.search,
            image=Global.get_ctk_cache_image("forum", "search.png", (24, 24)),
            width=24,
        )
        searchButton.pack(side="left", fill="y")
        Tooltip(searchButton, "Search")

        createPostButton = ctk.CTkButton(
            headerFrame,
            text="",
            fg_color="transparent",
            hover_color="#195a92",
            command=self.create_post,
            image=Global.get_ctk_cache_image("forum", "create_post.png", (24, 24)),
            width=24,
        )
        createPostButton.pack(side="left", fill="y")
        Tooltip(createPostButton, "Create Post")

        pfpPath = os.path.join(Global.CURRENT_PATH, "forum", "img", "pfp.png")
        customPfpPath = os.path.join(
            Global.CURRENT_PATH,
            "forum",
            "uploads",
            "pfp",
            f"{Global.forumAccount["id"]}.png",
        )
        pfp = circular_crop(
            customPfpPath if os.path.exists(customPfpPath) else pfpPath,
            24,
            24,
        )
        accountButton = ctk.CTkButton(
            headerFrame,
            text="",
            fg_color="transparent",
            hover_color="#195a92",
            command=self.account,
            image=pfp,
            width=24,
        )
        accountButton.pack(side="left", fill="y")
        Tooltip(accountButton, "Account")

    def search(self):
        """Perform a search using the keyword entered in the search bar.
        Navigates to the HomePage with the keyword as a filter.
        """

        keyword = self.searchInput.get()

        from forum.pages.HomePage import HomePage

        Global.pageManagers["forum"].clear_history()
        Global.pageManagers["forum"].show_page(HomePage, keyword)

    def create_post(self):
        """Navigate to the CreatePostPage.
        Opens the page where the user can create a new forum post.
        """

        from forum.pages.CreatePostPage import CreatePostPage

        Global.pageManagers["forum"].show_page(CreatePostPage)

    def account(self):
        """Navigate to the AccountPage.
        Opens the page where the user can view and manage their account.
        """

        from forum.pages.AccountPage import AccountPage

        Global.pageManagers["forum"].show_page(AccountPage)
