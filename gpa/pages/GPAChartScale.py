import customtkinter as ctk
from utils.core.Page import Page
from gpa.ui.Header import Header
from utils.ui.BackButton import BackButton
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from gpa.controllers.ProgrammeController import ProgrammeController
from utils.ui.Message import ErrorMessage



class GPAChartScalePage(Page):
    def __init__(self, parentFrame, id):
        super().__init__(parentFrame)
        self.id = id

    def load_content(self):
        # data 
        self.content = ProgrammeController.get_semesters_by_programme(self.id)
        
        if self.content is None: 
            ErrorMessage("GPA Chart Scale not found") 
        return False
        
    def create_UI(self):
        self.load_content()

        Header(self._frame, "GPA Chart Scale")

        contentFrame = ctk.CTkFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        contentFrame.pack(fill="both", expand=True)

        BackButton(contentFrame).pack(pady=10, padx=10, anchor="w")
        
        gradeFrame = ctk.CTkFrame(
            contentFrame, corner_radius=0, fg_color="black"
            )
        gradeFrame.pack(fill="both", expand=True)
        
        # data
        semesters = [semester["name"] for semester in self.content]
        gpas = [semester["gpa"] for semester in self.content]

        # Create a Matplotlib figure
        fig = Figure(figsize=(5,3), facecolor="#ebebeb")
        ax = fig.add_subplot(111)
        ax.bar(semesters, gpas, color='blue')
        ax.set_title("GPA Over Semesters")
        ax.set_xlabel("Semester")
        ax.set_ylabel("GPA")
        ax.grid(True)

        # Embed the plot in your *existing* CTk frame
        canvas = FigureCanvasTkAgg(fig, master=gradeFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
   