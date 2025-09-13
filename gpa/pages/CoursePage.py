from gpa.ui.Header import Header
from utils.ui.BackButton import BackButton
from utils.ui.DeleteButton import DeleteButton
from gpa.ui.SelectionItem import SelectionItem
from utils.core.Page import Page
import utils.core.Global as Global
from utils.ui.SaveButton import SaveButton
from utils.ui.Message import ErrorMessage, ConfirmationMessage

import customtkinter as ctk

from gpa.controllers.CourseworkController import CourseworkController
from gpa.controllers.CourseController import CourseController


class CoursePage(Page):
    def __init__(self, parentFrame, id):
        super().__init__(parentFrame)
        self.id = id
        
        
    def load_data(self):
        self.content = CourseController.get_course_public_data(self.id)

        if self.content is None:
            ErrorMessage("Course not found")
            return False

        self.courseworks = CourseController.get_courseworks_by_course(self.id)

    def create_UI(self):
        self.header = Header(self._frame, self.content["name"])

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
            actionFrame, placeholder_text="Enter course name", width=200
        )
        self.nameEntry.pack(side="left")
        self.nameEntry.insert(0, self.content["name"])

        # Delete Button
        DeleteButton(
            actionFrame,
            callback=lambda: ConfirmationMessage(
                "Are you sure you want to delete this course?",
                callback=self.delete_course,
            ),
            tooltipText="Delete Course",
        ).pack(side="right")

        # Courseworks
        for coursework in self.courseworks:
            SelectionItem(
                self.contentFrame,
                coursework["name"],
                (coursework["weight"] * coursework["score"]/100),
                callback=lambda id=coursework["id"]: self.navigate_to_coursework(id),
            )

        # Add Coursework Button
        SelectionItem(
            self.contentFrame,
            addButton=True,
            tooltipText="Add new coursework",
            callback=self.add_coursework,
        )

        # General Info
        self.generalFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        self.generalFrame.pack(fill="x", padx=10, pady=(50, 30))
        
        # Total Coursework Score
        ctk.CTkLabel(
            self.generalFrame,
            text="Total Coursework Score",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            self.generalFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=1, sticky="w")
        self.totalCourseworkScore = ctk.CTkLabel(
            self.generalFrame,
            font=("Segoe UI", 13),
        )
        self.totalCourseworkScore.grid(row=0, column=2, sticky="w")
        self.update_total_coursework_score()
        


        # Coursework Weight
        ctk.CTkLabel(
            self.generalFrame,
            text="Coursework Weight",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(
            self.generalFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=1, sticky="w")
        self.courseworkWeightEntry = ctk.CTkEntry(
            self.generalFrame, placeholder_text="", width=50
        )
        self.courseworkWeightEntry.grid(row=1, column=2, sticky="w")
        ctk.CTkLabel(
            self.generalFrame,
            text="%",
            font=("Segoe UI", 13),
        ).grid(row=1, column=3, sticky="w", padx=5)
        self.courseworkWeightEntry.insert(0, self.content["coursework_weight"])

        # Credit Hours
        ctk.CTkLabel(
            self.generalFrame,
            text="Credit Hours",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=0, sticky="w", pady=5)
        ctk.CTkLabel(
            self.generalFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=1, sticky="w", pady=5)
        self.creditHoursEntry = ctk.CTkEntry(
            self.generalFrame, placeholder_text="", width=50
        )
        self.creditHoursEntry.grid(row=2, column=2, sticky="w", pady=5)
        ctk.CTkLabel(
            self.generalFrame,
            text="Hour(s)",
            font=("Segoe UI", 13),
        ).grid(row=2, column=3, sticky="w", padx=5)
        self.creditHoursEntry.insert(0, self.content["credit_hours"])

        # Final Assessment
        self.finalAssessmentVar = ctk.StringVar(value="on" if self.content["has_final"] else "off")
        ctk.CTkLabel(
            self.generalFrame,
            text="Has Final Assessment",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=3, column=0, sticky="w")
        ctk.CTkLabel(
            self.generalFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=3, column=1, sticky="w")
        ctk.CTkSwitch(
            self.generalFrame,
            text="",
            font=("Segoe UI", 13, "bold"),
            variable=self.finalAssessmentVar,
            command=self.final_assessment_switch,
            onvalue="on",
            offvalue="off",
            width=20,
        ).grid(row=3, column=2, sticky="w", pady=(5, 0))

        # Predict Frame
        self.predictFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        self.predictFrame.pack(fill="x", padx=10, pady=(0, 30))
        if not self.content["has_final"]:
            self.predictFrame.pack_forget()

        # Predict Frame Title
        ctk.CTkLabel(
            self.predictFrame,
            text="Predict Final Assessment",
            font=("Segoe UI", 15, "bold", "underline"),
            text_color="black",
        ).grid(columnspan=3, sticky="w")

        # Desired Grade
        self.desiredGradeVar = ctk.BooleanVar(value="on")
        ctk.CTkLabel(
            self.predictFrame,
            text="Desired Grade",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(
            self.predictFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=1, sticky="w")
        self.desiredGradeCombo = ctk.CTkComboBox(
            self.predictFrame,
            values=["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F"],
            width=70,
        )
        
        self.desiredGradeCombo.grid(row=1, column=2, sticky="w")
        self.desiredGradeCombo.set(self.content["desired_grade"])
        

        

        # Final Assessment Score
        ctk.CTkLabel(
            self.predictFrame,
            text="Final Exam Target ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=0, sticky="w")
        ctk.CTkLabel(
            self.predictFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=1, sticky="w")
        self.finalAssessmentScore = ctk.CTkLabel(
            self.predictFrame,
            text="0%",
            font=("Segoe UI", 13),
        )
        self.finalAssessmentScore.grid(row=2, column=2, sticky="w")
        self.finalAssessmentScore.configure(text=f"{CourseController.get_predicted_grade_final_assessment_score(self.id)}")

        # Result Frame
        resultFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        resultFrame.pack(fill="x", padx=10, pady=(0, 10))

        # Result Frame Title
        ctk.CTkLabel(
            resultFrame,
            text="Result",
            font=("Segoe UI", 15, "bold", "underline"),
            text_color="black",
        ).grid(columnspan=3, sticky="w")

        # Grade
        ctk.CTkLabel(
            resultFrame,
            text="Grade",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(
            resultFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=1, column=1, sticky="w")
        self.resultGradeCombo = ctk.CTkComboBox(
            resultFrame,
            values=["-","A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F"],
            command=self.result_grade,
            width=70,
        )
        self.resultGradeCombo.grid(row=1, column=2, sticky="w")
        self.resultGradeCombo.set(self.content["grade"])
        

        # Grade Point
        ctk.CTkLabel(
            resultFrame,
            text="Grade Point",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=0, sticky="w")
        ctk.CTkLabel(
            resultFrame,
            text=":   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=1, sticky="w")
        self.resultGradePointLabel = ctk.CTkLabel(
            resultFrame,
            text = "4.0",
            font=("Segoe UI", 13),
        )
        self.resultGradePointLabel.grid(row=2, column=2, sticky="w")
        self.resultGradePointLabel.configure(text=f"{CourseController.get_grade_point_from_grade(self.id,  self.content["grade"])}")

        # Save Changes Button
        self.saveChangesButton = SaveButton(
            self.contentFrame, self.save_changes, self.is_changed
        )
        self.saveChangesButton.pack(padx=10, pady=(0, 30), anchor="w")
        # Save Changes
        for entry in (self.nameEntry, self.courseworkWeightEntry, self.creditHoursEntry):
            entry.bind("<KeyRelease>", lambda event: self.saveChangesButton.update_state())

        # ComboBoxes → use command
        self.desiredGradeCombo.configure(command=self.desired_grade)
        self.resultGradeCombo.configure(command=self.result_grade)



    def is_changed(self):
        course_info = {
            "name": self.nameEntry.get(),
            "coursework_weight": self.courseworkWeightEntry.get(),
            "credit_hours": self.creditHoursEntry.get(),
            "has_final": self.finalAssessmentVar.get() == "on",
            "desired_grade": self.desiredGradeCombo.get(),
            "grade": self.resultGradeCombo.get(),
        }
        
        return course_info != {
            "name": self.content["name"],
            "coursework_weight": str(self.content["coursework_weight"]),
            "credit_hours": str(self.content["credit_hours"]),
            "has_final":  bool(self.content["has_final"]),
            "desired_grade": self.content["desired_grade"],
            "grade": self.content["grade"],
        }

    def save_changes(self):
        course_info = {
            "name": self.nameEntry.get().strip(),
            "coursework_weight": self.courseworkWeightEntry.get(),
            "credit_hours": self.creditHoursEntry.get(),
            "has_final": self.finalAssessmentVar.get() == "on",
            "desired_grade": self.desiredGradeCombo.get(),
            "grade": self.resultGradeCombo.get(),
        }

        # Call controller to save changes
        returnValue = CourseController.edit_course(
            self.content["id"],
            course_info["name"],
            course_info["coursework_weight"],
            course_info["credit_hours"],
            course_info["has_final"],
            course_info["desired_grade"],
            course_info["grade"],
        )

        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.pageManagers["gpa"].currentPage.refresh_frame()

    def delete_course(self):
        error = CourseController.delete_course(self.content["id"])
        if isinstance(error, str):
            ErrorMessage(error)
            return

        Global.pageManagers["gpa"].back()
        

    def add_coursework(self):
        returnValue = CourseworkController.create_coursework(self.id)
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        self.navigate_to_coursework(returnValue["id"])

    def navigate_to_coursework(self, id):
        from gpa.pages.CourseworkPage import CourseworkPage

        Global.pageManagers["gpa"].show_page(CourseworkPage, id)

    def final_assessment_switch(self):
        if self.finalAssessmentVar.get() == "on":
            self.predictFrame.pack(
                after=self.generalFrame, fill="x", padx=10, pady=(0, 30)
            )
        else:
            self.predictFrame.pack_forget()
        self.saveChangesButton.update_state()

    def update_total_coursework_score(self):
        score = CourseController.get_coursework_score(self.id)
        self.totalCourseworkScore.configure(text=f"{score}%")


    def desired_grade(self, option=None):
        if option is None:
            option = self.desiredGradeCombo.get()  # current selection

        self.saveChangesButton.update_state()


    def result_grade(self, option=None):
        if option is None:
            option = self.resultGradeCombo.get() 
        self.resultGradePointLabel.configure(text=f"{CourseController.get_grade_point_from_grade(self.id, option)}")
        self.saveChangesButton.update_state()
