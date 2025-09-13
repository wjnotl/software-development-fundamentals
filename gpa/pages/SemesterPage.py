from gpa.entities.Semester import Semester
from gpa.ui.Header import Header
from gpa.ui.SelectionItem import SelectionItem
import utils.core.Global as Global
from utils.core.Page import Page
from utils.ui.BackButton import BackButton
from utils.ui.SaveButton import SaveButton
from utils.ui.DeleteButton import DeleteButton
from utils.ui.Message import ErrorMessage, ConfirmationMessage

from gpa.controllers.SemesterController import SemesterController
from gpa.controllers.CourseController import CourseController

import customtkinter as ctk


class SemesterPage(Page):
    def __init__(self, parentFrame, id):
        super().__init__(parentFrame)
        self.id = id

    def load_data(self):
        self.content = SemesterController.get_semester_public_data(self.id)

        if self.content is None:
            ErrorMessage("Semester not found")
            return False
        
        self.courses = SemesterController.get_courses_by_semester(self.id)

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
            actionFrame, placeholder_text="Enter semester name", width=200
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
                "Are you sure you want to delete this Semester?",
                callback=self.delete_semester,
            ),
            tooltipText="Delete Semester",
            ).pack(side="right")


        # Courses
        for course in self.courses:
            SelectionItem(
                self.contentFrame,
                course["name"],
                course["grade"],
                callback=lambda id=course["id"]: self.navigate_to_course(id),
            )

        # Add Course Button
        SelectionItem(
            self.contentFrame,
            addButton=True,
            tooltipText="Add new course",
            callback=self.add_course,
        )

        # Results
        resultFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        resultFrame.pack(fill="x", expand=True, padx=10, pady=(50, 10))

        # GPA
        ctk.CTkLabel(
            resultFrame,
            text="GPA",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            resultFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=1, sticky="w")
        self.gpa_entries = ctk.CTkLabel(
            resultFrame,
            text="4.0000",
            font=("Segoe UI", 13),
        )
        self.gpa_entries.grid(row=0, column=2, sticky="w")
        total_gpa = SemesterController.get_total_gpa(self.id)
        self.gpa_entries.configure(text=total_gpa)

        # Credits Earned
        ctk.CTkLabel(
            resultFrame,
            text="Credits Earned",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(
            resultFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=1, sticky="w")
        self.credit_entries = ctk.CTkLabel(
            resultFrame,
            text="0",
            font=("Segoe UI", 13),
        )
        self.credit_entries.grid(row=1, column=2, sticky="w")
        total_credits = SemesterController.get_total_credit(self.id)
        self.credit_entries.configure(text=total_credits)


        # Save Changes
        self.saveChangesButton = SaveButton(
            self.contentFrame, self.save_changes, self.is_changed
        )
        self.saveChangesButton.pack(padx=10, pady=(0, 30), anchor="w")

        self.nameEntry.bind("<KeyRelease>", lambda event: self.saveChangesButton.update_state())

    def is_changed(self):
        return self.content["name"] != self.nameEntry.get()

    def save_changes(self):
        returnValue = SemesterController.edit_semester(
            self.content["id"], self.nameEntry.get()
        )
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.pageManagers["gpa"].currentPage.refresh_frame()

    def delete_semester(self):
        error = SemesterController.delete_semester(self.content["id"])
        if isinstance(error, str):
            ErrorMessage(error)
            return

        Global.pageManagers["gpa"].back()

    def add_course(self):
        returnValue = CourseController.create_course(self.id)
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return
        
        self.navigate_to_course(returnValue["id"])

    def navigate_to_course(self, id):
        from gpa.pages.CoursePage import CoursePage

        Global.pageManagers["gpa"].show_page(CoursePage, id)