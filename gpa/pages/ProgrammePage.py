from gpa.ui.Header import Header
from gpa.ui.SelectionItem import SelectionItem
from utils.ui.BackButton import BackButton
from utils.ui.DeleteButton import DeleteButton
import utils.core.Global as Global
from utils.ui.Message import ErrorMessage, ConfirmationMessage
from utils.ui.SaveButton import SaveButton

from gpa.controllers.ProgrammeController import ProgrammeController
from gpa.controllers.SemesterController import SemesterController

import customtkinter as ctk
from utils.core.Page import Page


class ProgrammePage(Page):
    def __init__(self, parentFrame, id):
        super().__init__(parentFrame)
        self.id = id

    def load_data(self):
        self.content = ProgrammeController.get_programme_public_data(self.id)

        if self.content is None:
            Global.pageManagers["gpa"].back()
            ErrorMessage("Programme not found")
            return False
        
        self.semesters = ProgrammeController.get_semesters_by_programme(self.id)

    def create_UI(self):
        Header(self._frame, self.content["name"])

        self.contentFrame = ctk.CTkScrollableFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        self.contentFrame.pack(fill="both", expand=True)

        # Back Button
        BackButton(self.contentFrame, self.is_changed).pack(pady=10, anchor="w")

        # Action Frame
        actionFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        actionFrame.pack(fill="x", padx=10, pady=10)

        # Name
        ctk.CTkLabel(
            actionFrame,
            text="Name:",
            text_color="black",
            font=("Segoe UI", 13),
            anchor="w",
        ).pack(side="left", padx=(0, 8))

        self.nameEntry = ctk.CTkEntry(
            actionFrame, placeholder_text="Enter programme name", width=200
        )
        self.nameEntry.pack(side="left")
        self.nameEntry.insert(0, self.content["name"])

        # Delete Button
        if (
            self.content["id"] == self.content["id"]
        ):
            DeleteButton(
                actionFrame,
                callback=lambda: ConfirmationMessage(
                    "Are you sure you want to delete this Programme?",
                    callback=self.delete_programme,
                ),
                tooltipText="Delete Programme",
            ).pack(side="right")


        # Semesters
        for semester in self.semesters:
            SelectionItem(
                self.contentFrame,
                semester["name"],
                f"{semester["gpa"]:.4f}",
                callback=lambda id=semester["id"]: self.navigate_to_semester(id),
            )
        # Add Semester Button
        SelectionItem(
            self.contentFrame,
            addButton=True,
            tooltipText="Add new semester",
            callback=self.add_semester,
        )

        # Results
        resultFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        resultFrame.pack(fill="x", expand=True, padx=10, pady=(50, 0))

        # CGPA
        ctk.CTkLabel(
            resultFrame,
            text="CGPA",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            resultFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(
            resultFrame,
            text=f"{self.content["cgpa"]:.4f}",
            font=("Segoe UI", 13),
        ).grid(row=0, column=2, sticky="w")

        # Total Credits Earned
        ctk.CTkLabel(
            resultFrame,
            text="Total Credits Earned",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(
            resultFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=1, sticky="w")
        ctk.CTkLabel(
            resultFrame,
            text=self.content["total_credit"],
            font=("Segoe UI", 13),
        ).grid(row=1, column=2, sticky="w")

        # GPA chart Scale
        chartButton = ctk.CTkButton(
            self.contentFrame,
            text="Show Chart",
            fg_color="#e67e22",
            hover_color="#b55c17",
            command=self.gpa_chart_scale,
            width=0,
        )
        chartButton.pack(padx=10, pady=(30, 10), anchor="w")


        # Edit Grade Scale
        editButton = ctk.CTkButton(
            self.contentFrame,
            text="Edit Grade Scale",
            fg_color="#195a92",
            hover_color="#123f66",
            command=self.edit_grade_scale,
            width=0,
        )
        editButton.pack(padx=10, pady=(0, 10), anchor="w")

        # Save Changes
        self.saveChangesButton = SaveButton(
            self.contentFrame, self.save_changes, self.is_changed
        )
        self.saveChangesButton.pack(padx=10, pady=(0, 30), anchor="w")

        self.nameEntry.bind(
            "<KeyRelease>", lambda event: self.saveChangesButton.update_state()
        )

    def is_changed(self):
        return self.content["name"] != self.nameEntry.get()

    def save_changes(self):
        returnValue = ProgrammeController.edit_programme(
            self.content["id"], self.nameEntry.get()
        )
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.pageManagers["gpa"].currentPage.refresh_frame()

    def delete_programme(self):
        error = ProgrammeController.delete_programme(self.content["id"])
        if isinstance(error, str):
            ErrorMessage(error)
            return

        Global.pageManagers["gpa"].back()

    def add_semester(self):
        returnValue = SemesterController.create_semester(self.id)
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return
        
        self.navigate_to_semester(returnValue["id"])

    def navigate_to_semester(self, id): 
        from gpa.pages.SemesterPage import SemesterPage

        Global.pageManagers["gpa"].show_page(SemesterPage, id)

    def gpa_chart_scale(self):
        from gpa.pages.GPAChartScale import GPAChartScalePage

        Global.pageManagers["gpa"].show_page(GPAChartScalePage, self.content["id"])

    def edit_grade_scale(self):
        from gpa.pages.EditGradeScalePage import EditGradeScalePage

        Global.pageManagers["gpa"].show_page(EditGradeScalePage, self.content["id"])
