import utils.core.Global as Global
from utils.core.Page import Page
from reminder.ui.Header import Header
import customtkinter as ctk

from reminder.controllers.ListController import ListController

from utils.ui.Message import ErrorMessage

from reminder.ui.HomeListContainer import HomeListContainer


class HomePage(Page):
    def load_data(self):
        self.lists = ListController.get_home_lists()

    def create_UI(self):
        Header(self._frame, "My Lists")

        self.contentFrame = ctk.CTkScrollableFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        self.contentFrame.pack(fill="both", expand=True)

        # Lists
        for list in self.lists:
            HomeListContainer(
                self.contentFrame,
                list["name"],
                callback=lambda listId=list["id"]: self.navigate_to_list(listId),
            )

        # Add List Button
        HomeListContainer(
            self.contentFrame,
            addButton=True,
            tooltipText="Add new list",
            callback=self.add_list,
        )

    def add_list(self):
        returnValue = ListController.create_list()
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        self.navigate_to_list(returnValue["id"])

    def navigate_to_list(self, id):
        from reminder.pages.ListPage import ListPage

        Global.pageManagers["reminder"].show_page(ListPage, id)
