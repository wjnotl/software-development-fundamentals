import customtkinter as ctk


class Page:
    def __init__(self, parentFrame, fg_color="#ebebeb"):
        self.__parentFrame = parentFrame
        self.__fg_color = fg_color

    def create_frame(self):
        self._frame = ctk.CTkFrame(self.__parentFrame, corner_radius=0, fg_color=self.__fg_color, width=380, height=650)
        self._frame.pack_propagate(False)
        self._frame.grid_propagate(False)
        self._frame.place(x=0, y=0)
        if self.load_data() == False: # If load data fails, back to previous page
            return True
        
        self.create_UI()

    def destroy_frame(self):
        self._frame.destroy()
        self._frame = None

    def refresh_frame(self):
        self.destroy_frame()
        self.create_frame()

    def create_UI(self):
        pass

    def load_data(self):
        pass
