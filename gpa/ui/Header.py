import customtkinter as ctk


class Header:
    def __init__(self, parentFrame, title=""):
        headerFrame = ctk.CTkFrame(
            parentFrame,
            fg_color="#195a92",
            corner_radius=0,
        )
        headerFrame.pack(fill="x")

        self.titleLabel = ctk.CTkLabel(
            headerFrame,
            text=title,
            text_color="white",
            font=("Segoe UI", 15, "bold"),
            justify="left",
            wraplength=345,
        )
        self.titleLabel.pack(ipady=15, ipadx=15, fill="x")
