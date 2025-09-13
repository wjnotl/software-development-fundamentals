import utils.core.Global as Global
import customtkinter as ctk
import home.App as home
import gpa.App as gpa
import reminder.App as reminder
import forum.App as forum
from PIL import Image
import os

# Create app window
app = Global.rootWindow

# Tabs
tabs = {"home": {}, "gpa": {}, "reminder": {}, "forum": {}}

# Set appearance
ctk.set_appearance_mode("light")

# Set geometry
app.geometry("380x700+0+0")
app.resizable(False, False)  # Disable resizing

# Set window title and icon
app.title("Student Assistant App")
app.iconbitmap(os.path.join(Global.CURRENT_PATH, "app.ico"))

# Set content frames
for tab in tabs:
    tabs[tab]["frame"] = ctk.CTkFrame(
        app,
        corner_radius=0,
        fg_color="transparent",
        width=380,
        height=650,
    )
    tabs[tab]["frame"].place(x=0, y=0)
    tabs[tab]["frame"].pack_propagate(False)
    tabs[tab]["frame"].grid_propagate(False)

# Set footer frame
footer_frame = ctk.CTkFrame(
    app, corner_radius=0, fg_color="white", border_width=0, width=380, height=50
)
footer_frame.place(x=0, y=650)
footer_frame.rowconfigure(0, weight=1)
footer_frame.columnconfigure((0, 1, 2, 3), weight=1)

# Get footer button images
for tab in tabs:
    tmpIcon = Image.open(os.path.join(Global.CURRENT_PATH, tab, "img", "app.jpg"))
    tabs[tab]["tab_image"] = ctk.CTkImage(tmpIcon, size=(30, 30))
    tmpIcon = Image.open(os.path.join(Global.CURRENT_PATH, tab, "img", "app_selected.jpg"))
    tabs[tab]["tab_selected_image"] = ctk.CTkImage(tmpIcon, size=(30, 30))


def switch_tab(switched_tab):
    Global.activeTab = switched_tab

    # Hide all frames
    for tab in tabs:
        tabs[tab]["frame"].place_forget()

    # Show selected frame
    tabs[switched_tab]["frame"].place(x=0, y=0)

    # Reset button images
    for tab in tabs:
        tabs[tab]["footer_button"].configure(image=tabs[tab]["tab_image"])

    # Change button image
    tabs[switched_tab]["footer_button"].configure(
        image=tabs[switched_tab]["tab_selected_image"]
    )

    # Reset label text color
    for tab in tabs:
        tabs[tab]["footer_button"].configure(text_color="#666666")

    # Change label text color
    tabs[switched_tab]["footer_button"].configure(text_color="#195a92")

    # Reset label text weight
    for tab in tabs:
        tabs[tab]["footer_button"].configure(font=("Segoe UI", 12, "normal"))

    # Change label text weight
    tabs[switched_tab]["footer_button"].configure(font=("Segoe UI", 12, "bold"))


# Set footer buttons
def create_footer_button(tab, column, text):
    current_tab = tabs[tab]

    current_tab["footer_button"] = ctk.CTkLabel(
        footer_frame,
        width=95,
        height=50,
        corner_radius=0,
        text=text,
        text_color="#666666",
        fg_color="transparent",
        image=current_tab["tab_image"],
        compound="top",
        cursor="hand2",
        font=("Segoe UI", 12, "normal"),
    )
    current_tab["footer_button"].grid(row=0, column=column, sticky="nswe")

    # Set button click event
    current_tab["footer_button"].bind("<Button-1>", lambda event: switch_tab(tab))


create_footer_button("home", 0, "Home")
create_footer_button("gpa", 1, "GPA")
create_footer_button("reminder", 2, "Reminder")
create_footer_button("forum", 3, "Forum")

# Preset to home tab
switch_tab("home")

# Load widgets to main frame
home.App(tabs["home"]["frame"], switch_tab)
gpa.App(tabs["gpa"]["frame"])
reminder.App(tabs["reminder"]["frame"])
forum.App(tabs["forum"]["frame"])

# Launch
app.mainloop()
