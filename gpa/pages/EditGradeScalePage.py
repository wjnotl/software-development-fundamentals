import customtkinter as ctk
from utils.core.Page import Page
from gpa.ui.Header import Header
from utils.ui.BackButton import BackButton

from utils.ui.SaveButton import SaveButton

from gpa.controllers.ProgrammeController import ProgrammeController
from utils.ui.Message import ErrorMessage

import utils.core.Global as Global

from gpa.ui.GradeScaleItem import GradeScaleItem


class EditGradeScalePage(Page):
    def __init__(self, parentFrame, id):
        super().__init__(parentFrame)
        self.id = id

    def load_content(self):
        self.content = ProgrammeController.get_programme_public_data(self.id)

        if self.content is None:
            ErrorMessage("Grade Scale not found")
            return False

    def create_UI(self):
        self.load_content()

        Header(self._frame, "Edit Grade Scale")

        contentFrame = ctk.CTkFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        contentFrame.pack(fill="both", expand=True)

        BackButton(contentFrame, self.is_changed).pack(pady=10, padx=10, anchor="w")

        gradeFrame = ctk.CTkFrame(contentFrame, corner_radius=0, fg_color="transparent")
        gradeFrame.pack(fill="x", padx=20, pady=10)

        # Grades
        self.gradeElements = []
        for index, (grade, data) in enumerate(self.content["grade_info"].items()):
            ele = GradeScaleItem(gradeFrame, grade, data[0], data[1], index)
            self.gradeElements.append(ele)
            ele.gradePointEntry.bind(
                "<KeyRelease>", lambda event: self.saveButton.update_state()
            )
            ele.gradeScoreEntry.bind(
                "<KeyRelease>", lambda event: self.saveButton.update_state()
            )

        # Save Button
        self.saveButton = SaveButton(
            contentFrame,
            self.save_changes,
            self.is_changed,
        )
        self.saveButton.pack(padx=10, pady=(0, 10), anchor="w")

    def is_changed(self):
        grade_info = {}
        for ele in self.gradeElements:
            gradePointEntry = ele.gradePointEntry.get()
            gradeScoreEntry = ele.gradeScoreEntry.get()

            try:
                gradePointEntry = float(gradePointEntry)
                gradeScoreEntry = int(gradeScoreEntry)
            except:
                pass

            grade_info[ele.grade] = [gradePointEntry, gradeScoreEntry]

        return grade_info != self.content["grade_info"]

    def save_changes(self):
        grade_info = {}
        for ele in self.gradeElements:
            gradePointEntry = ele.gradePointEntry.get()
            gradeScoreEntry = ele.gradeScoreEntry.get()
            grade_info[ele.grade] = [gradePointEntry, gradeScoreEntry]

        returnValue = ProgrammeController.edit_programme(
            self.content["id"], self.content["name"], grade_info
        )
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.pageManagers["gpa"].currentPage.refresh_frame()
