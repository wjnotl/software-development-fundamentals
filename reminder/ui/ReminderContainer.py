import customtkinter as ctk
import utils.core.Global as Global
from utils.ui.Tooltip import Tooltip


class ReminderContainer:
    def __init__(
        self,
        parentFrame,
        text="",
        activeState=True,
        dayText="",
        timeText="",
        recurring=False,
        finished=False,
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
            wraplength=320,
        )
        textLabel.pack(fill="both", expand=True, padx=10, pady=10)

        detailsFrame = None
        self.bellIcon = None
        self.dateLabel = None
        self.timeLabel = None
        if not addButton:
            # Details
            detailsFrame = ctk.CTkFrame(
                self.container,
                fg_color="transparent",
                corner_radius=0,
            )
            detailsFrame.pack(fill="x", padx=10, pady=(0, 10))

            # Bell Icon
            self.activeState = activeState
            self.bellIcon = ctk.CTkLabel(
                detailsFrame,
                text="",
                image=Global.get_ctk_cache_image(
                    "reminder",
                    ("bell.png" if self.activeState else "bell_off.png"),
                    (24, 24),
                ),
                width=24,
                height=24,
            )
            self.bellIcon.pack(side="left", padx=(0, 5))

            # Date Text
            self.dateLabel = ctk.CTkLabel(
                detailsFrame,
                text=dayText + " • ",
                text_color="#666666",
                font=(
                    ("Segoe UI", 12)
                    if not finished
                    else ("Segoe UI", 12, "normal", "overstrike")
                ),
                anchor="w",
            )
            self.dateLabel.pack(side="left")

            # Time Text
            self.timeLabel = ctk.CTkLabel(
                detailsFrame,
                text=timeText + ("   ⟳" if recurring else ""),
                text_color="#666666",
                font=(
                    ("Segoe UI", 12)
                    if not finished
                    else ("Segoe UI", 12, "normal", "overstrike")
                ),
                anchor="w",
            )
            self.timeLabel.pack(side="left")

        self.container.bind("<Enter>", self.hover)
        self.container.bind("<Leave>", self.unhover)

        # Set Button Click Event
        for widget in [
            textLabel,
            self.container,
            detailsFrame,
            self.dateLabel,
            self.timeLabel,
        ]:
            if widget:
                widget.bind("<Button-1>", lambda event: callback())
                if tooltipText:
                    Tooltip(widget, tooltipText)

        # Toggle Active
        if self.bellIcon:
            self.bellIcon.bind("<Button-1>", lambda event: self.toggle_active())

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
        pass

    def toggle_active(self):
        self.activeState = not self.activeState
        self.update_bell_icon()
        if hasattr(self, "toggleActiveCallback"):
            self.toggleActiveCallback(self.id)

    def update_bell_icon(self):
        self.bellIcon.configure(
            image=(
                Global.get_ctk_cache_image(
                    "reminder",
                    ("bell.png" if self.activeState else "bell_off.png"),
                    (24, 24),
                )
            )
        )
        

    def update_date_label(self, date):
        self.dateLabel.configure(text=date + " • ")

    def update_finished(self, finished):
        self.dateLabel.configure(
            font=(
                ("Segoe UI", 12)
                if not finished
                else ("Segoe UI", 12, "normal", "overstrike")
            ),
        )
        self.timeLabel.configure(
            font=(
                ("Segoe UI", 12)
                if not finished
                else ("Segoe UI", 12, "normal", "overstrike")
            ),
        )
