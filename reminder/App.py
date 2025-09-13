from reminder.data.ListData import ListData
import utils.core.Global as Global
from utils.core.PageManager import PageManager
from reminder.pages.HomePage import HomePage

from reminder.ui.Notification import Notification

from reminder.controllers.ReminderController import ReminderController
from reminder.data.ReminderData import ReminderData
from utils.processing.DatetimeProcessing import is_datetime_expired
from utils.ui.Message import ErrorMessage


def App(frame):
    load_data()

    error = schedule_reminders()
    if error:
        ErrorMessage(error)
    
 
    Global.pageManagers["reminder"] = PageManager(frame)
    Global.pageManagers["reminder"].show_page(HomePage)


def load_data():
    error = ListData.load()
    if error:
        ErrorMessage(error)

    error = ReminderData.load()
    if error:
        ErrorMessage(error)

def schedule_reminders():
    error = None

    for reminder in ReminderController.get_reminders_public_data():
        if not reminder["isActive"]: continue
        try:
            if reminder["isRecurring"]:
                reminder=ReminderController.next_recurring_date(reminder["id"])
                if isinstance(reminder, str):
                    raise Exception(reminder)

            Notification.schedule(reminder)
        except:
            error = "Error while scheduling some reminders"

    return error