import customtkinter as ctk
import utils.core.Global as Global
from utils.ui.Tooltip import Tooltip


class DeleteButton(ctk.CTkLabel):
    def __init__(self, parentFrame, callback=None, tooltipText=None):
        super().__init__(
            parentFrame,
            fg_color="transparent",
            text="",
            width=24,
            height=24,
            image=Global.get_ctk_cache_image("utils", "delete.png", (24, 24)),
            cursor="hand2",
        )
        self.callback = callback

        # Delete Button Effect
        self.bind("<Enter>", self.hover)
        self.bind("<Leave>", self.unhover)
        self.bind("<Button-1>", self.click)

        # Set Tooltip
        if tooltipText:
            Tooltip(self, tooltipText)

    def click(self, event):
        self.callback()

    def hover(self, event):
        self.configure(
            image=Global.get_ctk_cache_image("utils", "delete_red.png", (24, 24))
        )

    def unhover(self, event):
        self.configure(
            image=Global.get_ctk_cache_image("utils", "delete.png", (24, 24))
        )
