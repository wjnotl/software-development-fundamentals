import customtkinter as ctk

class GradeScaleItem:
    def __init__(self, parentFrame, grade="", points=0, scores=0, row=0):
        ctk.CTkLabel(parentFrame, text=grade, font=("Segoe UI", 13, "bold")).grid(
            row=row, column=0, pady=(0, 10), sticky="w"
        )
        ctk.CTkLabel(
            parentFrame,
            text=" :   ",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=row, column=1, pady=(0, 10))

        self.grade = grade

        self.gradePointEntry = ctk.CTkEntry(parentFrame, width=60)
        self.gradePointEntry.grid(row=row, column=2, pady=(0, 10))
        self.gradePointEntry.insert(0, points)

        self.gradeScoreEntry = ctk.CTkEntry(parentFrame, width=45)
        self.gradeScoreEntry.grid(row=row, column=3, pady=(0, 10), padx=(15, 5))
        self.gradeScoreEntry.insert(0, scores)

        ctk.CTkLabel(
            parentFrame,
            text="%",
            text_color="#666666",
            font=("Segoe UI", 13),
        ).grid(row=row, column=4, pady=(0, 10), sticky="w")
