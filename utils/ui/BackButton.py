import customtkinter as ctk
import utils.core.Global as Global
from utils.ui.Message import ConfirmationMessage


class BackButton(ctk.CTkButton):
    def __init__(self, parentFrame, check_is_changed=lambda: False):
        super().__init__(
            parentFrame,
            text="Back",
            fg_color="transparent",
            hover_color="#ebebeb",
            command=self.back,
            image=Global.get_ctk_cache_image("forum", "back.png", (12, 12)),
            font=("Segoe UI", 13, "bold"),
            text_color="#195a92",
            anchor="w",
            compound="left",
        )

        # Hover Back Button Effect
        self.bind("<Enter>", self.back_hover)
        self.bind("<Leave>", self.back_unhover)

        self.check_is_changed = check_is_changed

    def back(self):
        if self.check_is_changed():
            ConfirmationMessage(
                "You have unsaved changes. Are you sure you want to go back?",
                callback=lambda: Global.pageManagers[Global.activeTab].back(),
            )
            return
        
        Global.pageManagers[Global.activeTab].back()

        

    def back_hover(self, event):
        self.configure(font=("Segoe UI", 13, "bold", "underline"))

    def back_unhover(self, event):
        self.configure(font=("Segoe UI", 13, "bold"))
