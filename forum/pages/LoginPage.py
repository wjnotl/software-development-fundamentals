import customtkinter as ctk

from utils.core.Page import Page
import utils.core.Global as Global
from utils.ui.Message import ErrorMessage
from utils.processing.StorageProcessing import save_forum_account_token

from forum.ui.PasswordEntry import PasswordEntry
from forum.pages.HomePage import HomePage
from forum.controllers.AccountController import AccountController


class LoginPage(Page):
    def create_UI(self):
        """Create the header and the main content of the login page."""

        formFrame = ctk.CTkFrame(
            self._frame,
            corner_radius=7,
            fg_color="#ffffff",
            border_width=1,
            border_color="#666666",
        )
        formFrame.pack(expand=True)

        # Title
        ctk.CTkLabel(
            formFrame,
            text="Login",
            text_color="black",
            font=("Segoe UI", 20, "bold"),
            anchor="w",
        ).pack(padx=20, pady=20, fill="x")

        # Username
        ctk.CTkLabel(
            formFrame,
            text="Username",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(anchor="w", padx=20)

        self.usernameEntry = ctk.CTkEntry(
            formFrame, placeholder_text="Enter your username", width=200
        )
        self.usernameEntry.pack(anchor="w", padx=20)

        # Password
        ctk.CTkLabel(
            formFrame,
            text="Password",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(padx=20, pady=(20, 0), anchor="w")

        self.passwordEntry = PasswordEntry(
            formFrame, placeholder_text="Enter your password", width=200
        )
        self.passwordEntry.pack(padx=20)

        # Login Button
        ctk.CTkButton(
            formFrame,
            text="Login",
            fg_color="#195a92",
            border_color="#195a92",
            text_color="white",
            font=("Segoe UI", 14, "bold"),
            command=self.login,
            width=80,
            height=30,
            anchor="n",
        ).pack(padx=20, pady=(30, 0), anchor="w")

        # Register Redirection
        ctk.CTkLabel(
            formFrame,
            text="New User?",
            text_color="#666666",
            font=("Segoe UI", 15, "normal"),
        ).pack(padx=(20, 0), pady=(0, 20), side="left")
        newUserButton = ctk.CTkButton(
            formFrame,
            text="Register",
            fg_color="white",
            border_color="white",
            hover_color="white",
            text_color="#195a92",
            font=("Segoe UI", 14, "bold"),
            command=self.register,
            width=0,
        )
        newUserButton.pack(side="left", pady=(0, 20))

        # Hover Register Effect
        newUserButton.bind(
            "<Enter>",
            lambda event: newUserButton.configure(
                font=("Segoe UI", 14, "bold", "underline")
            ),
        )
        newUserButton.bind(
            "<Leave>",
            lambda event: newUserButton.configure(font=("Segoe UI", 14, "bold")),
        )

    def register(self):
        """Redirect to the register account page."""

        from forum.pages.RegisterPage import RegisterPage

        Global.pageManagers["forum"].clear_history()
        Global.pageManagers["forum"].show_page(RegisterPage)

    def login(self):
        """Process the user's login request."""

        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        returnValue = AccountController.process_login(username, password)
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.forumAccount = returnValue
        save_forum_account_token(returnValue["token"])
        Global.pageManagers["forum"].show_page(HomePage, "")
