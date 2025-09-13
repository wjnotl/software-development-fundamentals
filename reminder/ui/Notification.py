import threading
from datetime import datetime
from plyer import notification

from utils.processing.DatetimeProcessing import get_datetime_from_string
import utils.core.Global as Global

from reminder.controllers.ReminderController import ReminderController


class Notification:
    __timers = {}

    def schedule(reminder):
        delay = (
            get_datetime_from_string(reminder["nextDate"], reminder["time"])
            - datetime.now()
        ).total_seconds()
        if delay <= 0:
            return

        timer = threading.Timer(
            delay,
            lambda: Notification.notify(reminder),

        )
        timer.daemon = True
        timer.start()

        Notification.__timers[reminder["id"]] = timer

    def cancel(reminder):
        timer = Notification.__timers.pop(reminder["id"], None)
        if timer:
            timer.cancel()

    def reschedule(reminder):
        Notification.cancel(reminder)
        Notification.schedule(reminder)

    def notify(reminder):
        if reminder["isActive"]:
            notification.notify(title="Reminder", message=reminder["name"], timeout=10)
            Notification.__timers.pop(reminder["id"])
            Notification.notification_end(reminder)

    def notification_end(reminder):
        if reminder["isActive"] and ReminderController.can_be_activated(reminder["id"]) is False:
            ReminderController.toggle_active(reminder["id"])

        if reminder["isRecurring"]:
            updatedReminderDate=ReminderController.next_recurring_date(reminder["id"])
            if isinstance(updatedReminderDate, str):
                print(updatedReminderDate)
                return
            Notification.schedule(updatedReminderDate)

        currentPage = Global.pageManagers["reminder"].currentPage
        if hasattr(currentPage, "notification_end_callback"):
            currentPage.notification_end_callback(reminder["id"])
