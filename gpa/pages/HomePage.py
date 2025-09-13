import customtkinter as ctk

from gpa.ui.SelectionItem import SelectionItem
from gpa.ui.Header import Header
from utils.core.Page import Page
import utils.core.Global as Global

from utils.ui.Message import ErrorMessage

from gpa.controllers.ProgrammeController import ProgrammeController


class HomePage(Page):
    def load_data(self):
        self.programmes = ProgrammeController.get_home_programmes()

    def create_UI(self):
        Header(self._frame, "Programme List")

        self.contentFrame = ctk.CTkScrollableFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        self.contentFrame.pack(fill="both", expand=True)

        # Programmes
        for programme in self.programmes:
            SelectionItem(
                self.contentFrame,
                programme["name"],
                programme["cgpa"],
                callback=lambda id=programme["id"]: self.navigate_to_programme(id),
            )

        # Add Programme Button
        SelectionItem(
            self.contentFrame,
            addButton=True,
            tooltipText="Add new programme",
            callback=self.add_programme,
        )

    def add_programme(self):
        returnValue = ProgrammeController.create_programme()
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        self.navigate_to_programme(returnValue["id"])

    def navigate_to_programme(self, id):
        from gpa.pages.ProgrammePage import ProgrammePage

        Global.pageManagers["gpa"].show_page(ProgrammePage, id)
