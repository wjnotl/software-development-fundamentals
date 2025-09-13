import customtkinter as ctk
from utils.ui.Tooltip import Tooltip


class SelectionItem:
    def __init__(
        self,
        parentFrame,
        text="",
        resultText=None,
        tooltipText=None,
        addButton=False,
        callback=lambda: None,
    ):
        self.container = ctk.CTkFrame(
            parentFrame,
            corner_radius=8,
            fg_color="white",
            border_color="#d1d5db",
            border_width=1,
            cursor="hand2",
        )
        self.container.pack(pady=(10, 0), padx=10, fill="x")

        # Text
        textLabel = ctk.CTkLabel(
            self.container,
            text="+" if addButton else text,
            text_color="black",
            font=("Segoe UI", 13),
            anchor="center" if addButton else "w",
            justify="left",
            wraplength=320 - (55 if resultText else 0),
        )
        textLabel.pack(fill="both", expand=True, padx=10, pady=10, side="left")

        # Result Text
        resultLabel = None
        if resultText:
            resultLabel = ctk.CTkLabel(
                self.container,
                text=resultText,
                text_color="#666666",
                font=("Segoe UI", 13),
                anchor="w",
                width=45,
            )
            resultLabel.pack(fill="y", padx=(0, 10), pady=10, side="left")

        self.container.bind("<Enter>", self.hover)
        self.container.bind("<Leave>", self.unhover)

        # Set Button Click Event
        for widget in [
            textLabel,
            resultLabel,
            self.container,
        ]:
            if widget:
                widget.bind("<Button-1>", lambda event: callback())
                if tooltipText:
                    Tooltip(widget, tooltipText)

    def hover(self, event):
        self.container.configure(fg_color="#f7f7f7")

    def unhover(self, event):
        self.container.after(100, self.check_mouse_leave)

    def check_mouse_leave(self):
        widget_under_mouse = self.container.winfo_containing(
            self.container.winfo_pointerx(), self.container.winfo_pointery()
        )

        # Check if it's still inside self.container (or a child)
        parent = widget_under_mouse
        while parent is not None:
            if parent == self.container:
                return  # Still inside, do nothing
            parent = parent.master

        # Not inside anymore
        self.container.configure(fg_color="white")
