import os
import csv

import utils.core.Global as Global

from reminder.entities.Reminder import Reminder

from reminder.data.ListData import ListData


class ReminderData:
    __reminders = []

    # Getter
    def get_reminders():
        return tuple(ReminderData.__reminders)

    def get_reminder_by_id(id):
        for reminder in ReminderData.__reminders:
            if reminder.get_id() == id:
                return reminder
        return None

    # Method
    def add_reminder(reminder):
        ReminderData.__reminders.append(reminder)

    def remove_reminder(reminder):
        for rem in ReminderData.__reminders:
            if rem == reminder:
                ReminderData.__reminders.remove(rem)
                break

    # Storage
    def save():
        try:
            with open(
                os.path.join(
                    Global.CURRENT_PATH, "reminder", "storage", "reminders.csv"
                ),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for reminder in ReminderData.get_reminders():
                    data.append(
                        [
                            reminder.get_id(),
                            reminder.get_name(),
                            reminder.get_isActive(),
                            reminder.get_time(),
                            reminder.get_date(),
                            reminder.get_isRecurring(),
                            reminder.get_recurringNumber(),
                            reminder.get_recurringType(),
                            reminder.get_list().get_id(),
                        ]
                    )
                writer.writerows(data)

        except PermissionError:
            return "Permission denied while saving the file"

        except IOError as e:
            return "IOError: " + str(e)

        return None

    def load():
        try:
            path = os.path.join(
                Global.CURRENT_PATH, "reminder", "storage", "reminders.csv"
            )
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass

            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    list = ListData.get_list_by_id(int(row[8]))
                    if list:
                        reminder = Reminder(
                            int(row[0]),
                            row[1],
                            row[2] == "True",
                            row[3],
                            row[4],
                            row[5] == "True",
                            int(row[6]),
                            row[7],
                            list,
                        )
                        list.add_reminder(reminder)
                        ReminderData.__reminders.append(reminder)

        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return None
