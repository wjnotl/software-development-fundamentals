from datetime import datetime, time, date
from utils.processing.DatetimeProcessing import (
    add_date_delta,
    get_datetime_from_string,
    is_datetime_expired,
)

from reminder.entities.Reminder import Reminder
from reminder.data.ListData import ListData
from reminder.data.ReminderData import ReminderData


class ReminderController:
    # Getter
    def get_reminder_public_data(id):
        reminder = ReminderData.get_reminder_by_id(id)
        if reminder is None:
            return None

        return reminder.get_public_data()
    
    def get_reminders_public_data():
        return [reminder.get_public_data() for reminder in ReminderData.get_reminders()]

    # Create
    def create_reminder(listId, name, isActive, time, date, isRecurring, recurringNumber, recurringType):
        list = ListData.get_list_by_id(listId)
        if list is None:
            return "List not found"

        name = name.strip()
        error = ReminderController.__is_name_valid(name)
        if error: return error
        error = ReminderController.__is_active_valid(isActive)
        if error: return error
        error = ReminderController.is_time_valid(time)
        if error: return error
        error = ReminderController.is_date_valid(date)
        if error: return error
        error = ReminderController.__is_recurring_valid(isRecurring)
        if error: return error
        if isRecurring:
            error = ReminderController.__is_recurringNumber_valid(recurringNumber)
            if error: return error
            error = ReminderController.__is_recurringType_valid(recurringType)
            if error: return error
            recurringNumber=int(recurringNumber)
        else:
            recurringNumber = 1
            recurringType = "days"

        reminder = Reminder(
            ReminderController.get_next_id(),
            name, isActive, time, date, isRecurring,
            recurringNumber, recurringType, list
        )
        
        list.add_reminder(reminder)
        ReminderData.add_reminder(reminder)

        error = ReminderData.save()
        if error:
            return error
        
        error = ReminderController.next_recurring_date(reminder.get_id())
        if isinstance(error, str):
            return error

        return reminder.get_public_data()

    # Delete
    def delete_reminder(id):
        from reminder.ui.Notification import Notification
        reminder = ReminderData.get_reminder_by_id(id)
        if reminder is None:
            return "Reminder not found"
        
        Notification.cancel(reminder.get_public_data())

        remindersList = reminder.get_list()
        if remindersList:
            remindersList.remove_reminder(reminder)

        ReminderData.remove_reminder(reminder)
        error = ReminderData.save()
        if error:
            return error
        
        return "Reminder deleted"

    # Edit
    def edit_reminder(
        id, name, isActive, time, date, isRecurring, recurringNumber, recurringType
    ):
        reminder = ReminderData.get_reminder_by_id(id)
        if reminder is None:return "Reminder not found"

        name = name.strip()
        error = ReminderController.__is_name_valid(name)
        if error: return error
        error = ReminderController.__is_active_valid(isActive)
        if error: return error
        error = ReminderController.is_time_valid(time)
        if error: return error
        error = ReminderController.is_date_valid(date)
        if error: return error
        error = ReminderController.__is_recurring_valid(isRecurring)
        if error: return error
        if isRecurring:
            error = ReminderController.__is_recurringNumber_valid(recurringNumber)
            if error: return error
            recurringNumber=int(recurringNumber)
            error = ReminderController.__is_recurringType_valid(recurringType)
            if error: return error
        else:
            recurringNumber = 1
            recurringType = "days"

        reminder.set_name(name)
        reminder.set_isActive(isActive)
        reminder.set_time(
            get_datetime_from_string(time_str=time).time().strftime("%I:%M:%p")
        )
        reminder.set_date(
            get_datetime_from_string(date_str=date).date().strftime("%Y-%m-%d")
        )
        reminder.set_isRecurring(isRecurring)
        reminder.set_recurringNumber(recurringNumber)
        reminder.set_recurringType(recurringType)

        error = ReminderData.save()
        if error:
            return error
        
        error = ReminderController.next_recurring_date(reminder.get_id())
        if isinstance(error, str):
            return error

        return reminder.get_public_data()

    # Method
    def toggle_active(id):
        reminder = ReminderData.get_reminder_by_id(id)
        if reminder is None:
            return "Reminder not found"

        reminder.set_isActive(not reminder.get_isActive())

        error = ReminderData.save()
        if error:
            return error
        
        from reminder.ui.Notification import Notification
        content = reminder.get_public_data()
        if content["isActive"]:
            Notification.schedule(content)
        else:
            Notification.cancel(content)

        return content

    def can_be_activated(id):
        reminder = ReminderData.get_reminder_by_id(id)
        if reminder is None:
            return False

        print(is_datetime_expired(reminder.get_date(), reminder.get_time()))
        return reminder.get_isRecurring() is True or not is_datetime_expired(
            reminder.get_date(), reminder.get_time()
        )
    
    def reschedule_expired_recurring(id):
        reminder = ReminderData.get_reminder_by_id(id)
        if reminder is None:
            return "Reminder not found"

    # Utils
    def get_next_id():
        if not ReminderData.get_reminders():
            return 1

        return max(rem.get_id() for rem in ReminderData.get_reminders()) + 1

    # Validation
    def __is_name_valid(name):
        if name == "":
            return "Name cannot be empty"

        if len(name) > 50:
            return "Name cannot be longer than 50 characters"

        return None

    def __is_active_valid(isActive):
        if isActive is not True and isActive is not False:
            return "Toggle active must be either True or False"

        return None

    def is_time_valid(time):
        try:
            datetime.strptime(time, "%I:%M:%p")
        except:
            return "Time is invalid"

        return None

    def is_date_valid(date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            return "Date is invalid"

        return None

    def __is_recurring_valid(isRecurring):
        if isRecurring is not True and isRecurring is not False:
            return "Recurring must be either True or False"

        return None

    def __is_recurringNumber_valid(recurringNumber):
        if recurringNumber is None:
            return "Recurring number cannot be empty"
        
        try:
            recurringNumber = int(recurringNumber)
            if recurringNumber < 1:
                return "Recurring number must be greater than 0"
        except ValueError:
            return "Recurring number must be an integer"
        except:
            return "Unknown error"
        return None

    def __is_recurringType_valid(recurringType):
        if recurringType not in ["days", "weeks", "months", "years"]:
            return "Recurring type must be one of the following: days, weeks, months, years"

        return None

    def next_recurring_date(id):
        reminder = ReminderData.get_reminder_by_id(id)
        if reminder is None:
            return "Reminder not found"
        nextDate=reminder.get_next_date()
        nextDate=nextDate.strftime("%Y-%m-%d")
        reminder.set_date(nextDate)
        
        error=ReminderData.save()
        if error:
            return error
        return reminder.get_public_data()
    

        