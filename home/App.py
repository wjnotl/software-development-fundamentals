import utils.core.Global as Global
import os
import customtkinter as ctk
from PIL import Image

class AppContainer:
    def __init__(self, frame, tab, title, description, switch_tab):
        self.container = ctk.CTkFrame(
            frame,
            corner_radius=8,
            fg_color="white",
            border_color="#d1d5db",
            border_width=1,
            cursor="hand2",
        )
        self.container.pack(pady=(20, 0), padx=20, fill="x")

        # App Icon
        image = Image.open(os.path.join(Global.CURRENT_PATH, "home", "img", tab + ".png"))
        icon = ctk.CTkImage(image, size=(80, 80))
        iconLabel = ctk.CTkLabel(self.container, text="", image=icon)
        iconLabel.pack(side="left", pady=10, padx=(10, 0))

        # Text frame
        textFrame = ctk.CTkFrame(
            self.container,
            corner_radius=0,
            fg_color="transparent",
        )
        textFrame.pack(side="left", pady=10, padx=(0, 10), expand=True, fill="x")

        # Title
        titleLabel = ctk.CTkLabel(
            textFrame, text=title, text_color="#666666", font=("Segoe UI", 15, "bold")
        )
        titleLabel.pack(pady=(10, 0), anchor="w")

        # Description
        descriptionLabel = ctk.CTkLabel(
            textFrame,
            text=description,
            text_color="#666666",
            font=("Segoe UI", 12, "normal"),
        )
        descriptionLabel.pack(pady=(0, 10), anchor="w")

        # Set Hover Effect
        self.container.bind("<Enter>", self.hover)
        self.container.bind("<Leave>", self.unhover)

        # Set Button Click Event
        for widget in [
            iconLabel,
            titleLabel,
            descriptionLabel,
            textFrame,
            self.container,
        ]:
            widget.bind("<Button-1>", lambda event: switch_tab(tab))

    def hover(self, event):
        self.container.configure(fg_color="#f7f7f7")

    def unhover(self, event):
        self.container.after(100, self.check_mouse_leave)

    def check_mouse_leave(self):
        widget_under_mouse = self.container.winfo_containing(self.container.winfo_pointerx(), self.container.winfo_pointery())

        # Check if it's still inside self.container (or a child)
        parent = widget_under_mouse
        while parent is not None:
            if parent == self.container:
                return  # Still inside, do nothing
            parent = parent.master

        # Not inside anymore
        self.container.configure(fg_color="white")


def App(frame, switch_tab):
    titleFrame = ctk.CTkFrame(frame, corner_radius=0, fg_color="#195a92")
    titleFrame.pack(fill="x")

    titleLabel = ctk.CTkLabel(
        titleFrame,
        text="Student Assistant App",
        text_color="white",
        font=("Segoe UI", 20, "bold"),
    )
    titleLabel.pack(pady=(30, 0), fill="x")

    descriptionLabel = ctk.CTkLabel(
        titleFrame,
        text="The ultimate app for managing student life",
        text_color="white",
        font=("Segoe UI", 15, "normal"),
    )
    descriptionLabel.pack(pady=(0, 30), fill="x")

    AppContainer(
        frame, "gpa", "GPA Calculator", "Calculate and view your GPA easily", switch_tab
    )
    AppContainer(
        frame, "reminder", "Reminder App", "Set reminders for yourself", switch_tab
    )
    AppContainer(
        frame,
        "forum",
        "Study Forum",
        "Discuss questions and share your thoughts",
        switch_tab,
    )
