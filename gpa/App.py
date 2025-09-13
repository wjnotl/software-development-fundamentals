from gpa.pages.HomePage import HomePage
from utils.core.PageManager import PageManager

from gpa.data.ProgrammeData import ProgrammeData
from gpa.data.SemesterData import SemesterData
from gpa.data.CourseData import CourseData
from gpa.data.CourseworkData import CourseworkData

import utils.core.Global as Global
from utils.ui.Message import ErrorMessage

def App(frame):
    error = load_data()
    if error:
        ErrorMessage(error)

    Global.pageManagers["gpa"] = PageManager(frame)
    Global.pageManagers["gpa"].show_page(HomePage)

def load_data():
    error = ProgrammeData.load()
    if error:
        return error

    error = SemesterData.load()
    if error:
        return error

    error = CourseData.load()
    if error:
        return error
    
    error = CourseworkData.load()
    if error:
        return error
    
    return None