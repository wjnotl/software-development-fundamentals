import customtkinter as ctk
from utils.core.Page import Page
from gpa.ui.Header import Header
from utils.ui.BackButton import BackButton
from utils.ui.DeleteButton import DeleteButton
from utils.ui.SaveButton import SaveButton
from utils.ui.Message import ErrorMessage, ConfirmationMessage
import utils.core.Global as Global

from gpa.controllers.CourseworkController import CourseworkController


class CourseworkPage(Page):
    def __init__(self, parentFrame, id):
        super().__init__(parentFrame)
        self.id = id

    def load_data(self):
        self.content = CourseworkController.get_coursework_public_data(self.id)

        if self.content is None:
            ErrorMessage("Coursework not found")
            return False
        
        CourseworkController.get_courseworks_by_course(self.id)

    def create_UI(self):
        self.header = Header(self._frame, self.content["name"])

        self.contentFrame = ctk.CTkFrame(
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

        # General Info Frame
        generalFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        generalFrame.pack(fill="x", padx=10, pady=(0, 30))
        generalFrame.columnconfigure(0, weight=1)
        generalFrame.columnconfigure(1, weight=1)
        generalFrame.columnconfigure(2, weight=1)
        generalFrame.columnconfigure(3, weight=100)
        generalFrame.columnconfigure(4, weight=1)

        # Name
        ctk.CTkLabel(
            generalFrame,
            text="Name",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            generalFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=1, sticky="w")
        self.nameEntry = ctk.CTkEntry(
            generalFrame, placeholder_text="Enter coursework name", width=200
        )
        self.nameEntry.grid(row=0, column=2, columnspan=2, sticky="w")
        self.nameEntry.insert(0, self.content["name"])

        # Delete Button
        DeleteButton(
            actionFrame,
            callback=lambda: ConfirmationMessage(
                "Are you sure you want to delete this Coursework?",
                callback=self.delete_coursework,
            ),
            tooltipText="Delete Semester",
        ).pack(side="right")


        # Weight
        ctk.CTkLabel(
            generalFrame,
            text="Weight",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=0, sticky="w", pady=10)
        ctk.CTkLabel(
            generalFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=1, sticky="w", pady=10)
        self.weightEntry = ctk.CTkEntry(generalFrame, width=50)
        self.weightEntry.grid(row=1, column=2, sticky="w", pady=10)
        ctk.CTkLabel(
            generalFrame,
            text="%",
            font=("Segoe UI", 13),
            anchor="w",
        ).grid(row=1, column=3, sticky="w", pady=10)
        self.weightEntry.insert(0, self.content["weight"])

        # Score
        ctk.CTkLabel(
            generalFrame,
            text="Score",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=0, sticky="w")
        ctk.CTkLabel(
            generalFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=1, sticky="w")
        self.scoreEntry = ctk.CTkEntry(generalFrame, width=50)
        self.scoreEntry.grid(row=2, column=2, sticky="w")
        ctk.CTkLabel(
            generalFrame,
            text="%",
            font=("Segoe UI", 13),
        ).grid(row=2, column=3, sticky="w")
        self.scoreEntry.insert(0, self.content["score"])

        # Save Changes
        for entry in (self.nameEntry, self.weightEntry, self.scoreEntry):
            entry.bind("<KeyRelease>", lambda event: self.saveButton.update_state())

        # Save Button
        self.saveButton = SaveButton(
            self.contentFrame,
            self.save_changes,
            self.is_changed,
        )
        self.saveButton.pack(padx=10, pady=(0, 10), anchor="w")

    def save_changes(self):
        coursework_info = {
            "name": self.nameEntry.get().strip(),
            "weight": self.weightEntry.get(),
            "score": self.scoreEntry.get(),
        }

        # Call controller to save changes
        returnValue = CourseworkController.edit_coursework(
            self.content["id"],
            coursework_info["name"],
            coursework_info["weight"],
            coursework_info["score"],
        )

        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.pageManagers["gpa"].currentPage.refresh_frame()

    def is_changed(self):
        coursework_info = {
            "name": self.nameEntry.get(),
            "weight": self.weightEntry.get(),
            "score": self.scoreEntry.get(),
        }
        return coursework_info != {
            "name": self.content["name"],
            "weight": str(self.content["weight"]),
            "score": str(self.content["score"]),
        }

    def delete_coursework(self):
        error = CourseworkController.delete_coursework(self.content["id"])
        if isinstance(error, str):
            ErrorMessage(error)
            return

        Global.pageManagers["gpa"].back()
    
    
