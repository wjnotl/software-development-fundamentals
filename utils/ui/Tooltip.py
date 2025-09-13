import tkinter as tk


class Tooltip:
    def __init__(self, widget, text, x_offset=10, y_offset=10):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.mouse_x = 0
        self.mouse_y = 0
        self.inside_widget = False

        widget.bind("<Enter>", self.on_widget_enter)
        widget.bind("<Leave>", self.on_widget_leave)

    def on_widget_enter(self, event):
        self.inside_widget = True
        self.mouse_x = event.x_root
        self.mouse_y = event.y_root
        self.widget.bind("<Motion>", self.track_mouse)
        self.widget.after(500, self.check_show)

    def on_widget_leave(self, event):
        self.inside_widget = False
        self.widget.unbind("<Motion>")
        self.widget.after(100, self.check_hide)

    def track_mouse(self, event):
        self.mouse_x = event.x_root
        self.mouse_y = event.y_root

    def show_tooltip(self):
        if self.tip_window or not self.text:
            return

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(
            True
        )  # Remove window decorations (title bar, border, close/minimize buttons)
        self.tip_window.wm_geometry(
            f"+{self.mouse_x + self.x_offset}+{self.mouse_y + self.y_offset}"
        )
        self.tip_window.attributes("-topmost", True)  # Stay on top of all other windows

        label = tk.Label(
            self.tip_window,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 11),
        )
        label.pack(ipadx=5, ipady=2)

    def check_show(self):
        if self.inside_widget:
            self.show_tooltip()

    def check_hide(self):
        if not self.inside_widget:
            self.hide_tooltip()

    def hide_tooltip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
