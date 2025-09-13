import customtkinter as ctk

class SaveButton(ctk.CTkButton):
    def __init__(self, master, save_changes_callback=lambda: None, is_changed_callback=lambda: None):
        super().__init__(
            master,
            text="Save Changes",
            fg_color="#2CC985",
            hover_color="#0C955A",
            text_color="gray98",
            text_color_disabled="gray78",
            command=save_changes_callback,
            width=0,
            state="disabled",
        )

        self.is_changed_callback = is_changed_callback

    def update_state(self):
        self.configure(
            state=(
                "normal"
                if self.is_changed_callback()
                else "disabled"
            )
        )