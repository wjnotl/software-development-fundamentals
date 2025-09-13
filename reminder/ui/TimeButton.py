import customtkinter as ctk
import utils.core.Global as Global
from utils.ui.Tooltip import Tooltip


class TimeButton(ctk.CTkLabel):
    def __init__(self, parentFrame, upButton=True, callback=None, tooltipText=None):
        super().__init__(
            parentFrame,
            text="",
            text_color="black",
            font=("Segoe UI", 13),
            cursor="hand2",
            image=Global.get_ctk_cache_image(
                "reminder", "up.png" if upButton else "down.png", (24, 24)
            ),
            width=24,
            height=24,
        )

        self.bind("<Button-1>", lambda event: callback())
        if tooltipText:
            Tooltip(self, tooltipText)
