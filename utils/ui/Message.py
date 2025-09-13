import utils.core.Global as Global

import customtkinter as ctk


class Overlay:
    def __init__(self):
        self.overlay = ctk.CTkFrame(
            Global.rootWindow,
            width=380,
            height=700,
            fg_color="transparent",
        )
        self.overlay.place(x=0, y=0)
        self.overlay.pack_propagate(False)

        self.frame = ctk.CTkFrame(
            self.overlay,
            fg_color="transparent",
        )
        self.frame.pack(expand=True, fill="x")
        self.frame.pack_propagate(False)
        self.frame.grid_propagate(False)

    def remove_overlay(self):
        self.overlay.destroy()
        self.overlay = None


class ConfirmationMessage:
    def __init__(
        self,
        text,
        confirm_color="#2CC985",
        confirm_hover_color="#0C955A",
        cancel_color="red1",
        cancel_hover_color="red3",
        callback=lambda: None,
    ):
        self.callback = callback

        # Overlay
        self.overlay = Overlay()

        # Message
        ctk.CTkLabel(
            self.overlay.frame,
            text=text,
            text_color="black",
            font=("Segoe UI", 15, "bold"),
            wraplength=340,
            justify="left",
        ).pack(pady=(0, 10), padx=20, fill="x", expand=True, anchor="s")

        # Button Frame
        buttonFrame = ctk.CTkFrame(self.overlay.frame, corner_radius=0, fg_color="transparent")
        buttonFrame.pack(padx=20, expand=True, anchor="n")

        # Confirm button
        ctk.CTkButton(
            buttonFrame,
            text="Yes",
            fg_color=confirm_color,
            hover_color=confirm_hover_color,
            font=("Segoe UI", 14, "bold"),
            width=50,
            command=self.confirm,
        ).pack(side="left", padx=5, ipady=2)

        # Cancel button
        ctk.CTkButton(
            buttonFrame,
            text="No",
            fg_color=cancel_color,
            hover_color=cancel_hover_color,
            font=("Segoe UI", 14, "bold"),
            width=50,
            command=self.cancel,
        ).pack(side="right", padx=5, ipady=2)

    def confirm(self):
        self.overlay.remove_overlay()
        self.callback()

    def cancel(self):
        self.overlay.remove_overlay()


class ErrorMessage:
    def __init__(self, text):
        # Overlay
        self.overlay = Overlay()

        # Message
        ctk.CTkLabel(
            self.overlay.frame,
            text=text,
            text_color="black",
            font=("Segoe UI", 15, "bold"),
            wraplength=340,
            justify="left",
        ).pack(pady=(0, 10), padx=20, fill="x", expand=True, anchor="s")

        # Okay button
        ctk.CTkButton(
            self.overlay.frame,
            text="Okay",
            font=("Segoe UI", 14, "bold"),
            width=50,
            command=self.overlay.remove_overlay,
        ).pack(padx=5, ipady=2, expand=True, anchor="n")