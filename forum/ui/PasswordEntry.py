import customtkinter as ctk

import utils.core.Global as Global


class PasswordEntry(ctk.CTkFrame):
    """A custom entry widget with a toggleable password visibility button.
    Inherits from CTkFrame, and contains:
    - A CTkEntry for typing passwords.
    - A CTkButton to toggle showing/hiding the password.
    """

    def __init__(self, master=None, **kwargs):
        """Initialize the PasswordEntry widget.
        :param master: Parent widget.
        :param kwargs: Extra keyword arguments for CTkEntry.
        """

        super().__init__(master, fg_color="transparent")
        self.visible = False

        self.entry = ctk.CTkEntry(self, show="•", **kwargs)
        self.entry.pack(side="left")

        self.toggle_btn = ctk.CTkButton(
            self,
            text="",
            image=Global.get_ctk_cache_image("forum", "eye.png", (20, 20)),
            width=20,
            fg_color="white",
            hover_color="white",
            command=self.toggle,
        )
        self.toggle_btn.pack(side="left")

    def toggle(self):
        """Toggle password visibility between hidden (•) and plain text."""

        self.visible = not self.visible
        self.entry.configure(show="" if self.visible else "•")
        self.toggle_btn.configure(
            image=(
                Global.get_ctk_cache_image("forum", "eye_closed.png", (20, 20))
                if self.visible
                else Global.get_ctk_cache_image("forum", "eye.png", (20, 20))
            )
        )

    def get(self):
        """Return the current text from the entry."""

        return self.entry.get()

    def insert(self, index, text):
        """Insert text at the given index.
        :param index: Position to insert the text.
        :param text: The string to insert.
        """

        self.entry.insert(index, text)

    def delete(self, first, last=None):
        """Delete text between the given indices.
        :param first: Starting index.
        :param last: Optional ending index (defaults to first if not given).
        """

        self.entry.delete(first, last)
