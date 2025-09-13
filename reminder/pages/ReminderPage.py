from datetime import date, timedelta, time
from reminder.ui.Notification import Notification
import utils.core.Global as Global
from utils.core.Page import Page
from utils.processing.DatetimeProcessing import (
    get_datetime_from_string,
    get_time_from_string,
)
from utils.ui.SaveButton import SaveButton
from utils.ui.BackButton import BackButton
from utils.ui.DeleteButton import DeleteButton
from utils.ui.Message import ConfirmationMessage, ErrorMessage
from reminder.ui.Header import Header

import customtkinter as ctk
from tkcalendar import Calendar

from reminder.ui.TimeButton import TimeButton

from reminder.controllers.ReminderController import ReminderController


class ReminderPage(Page):
    def __init__(self, parentFrame, id, listId=None):
        super().__init__(parentFrame)
        self.id = id
        self.listId = listId
        self.isNew = self.id == -1 

    def load_data(self):
        if self.isNew:
            self.content = {
                "id": -1,
                "name": f"Untitled Reminder {ReminderController.get_next_id()}",
                "isActive": True,
                "time": time(7, 0).strftime("%I:%M:%p"),
                "date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "isRecurring": False,
                "recurringNumber": 1,
                "recurringType": "days"
            }
            self.content["nextDate"] = self.content["date"]
        else:
            self.content = ReminderController.get_reminder_public_data(self.id)

        if self.content is None:
            ErrorMessage("Reminder not found")
            return False
        return True

    def create_UI(self):
        self.header = Header(self._frame, self.content["name"])
        self.contentFrame = ctk.CTkFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        self.contentFrame.pack(fill="both", expand=True)

        # Back Button
        BackButton(self.contentFrame, self.is_changed).pack(pady=10, padx=10, anchor="w")

        # Activate Reminder Switch
        self.activateReminderSwitch = ctk.CTkSwitch(
            self.contentFrame,
            text="Active",
            command=self.toggle_active,
        )
        self.activateReminderSwitch.pack(padx=20, pady=(20, 0), anchor="w")
        if self.content["isActive"]:
            self.activateReminderSwitch.select()

        # Action Frame
        actionFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        actionFrame.pack(fill="x", padx=20, pady=10)

        # Name
        ctk.CTkLabel(
            actionFrame,
            text="Name:",
            text_color="black",
            font=("Roboto", 13),
            anchor="w",
        ).pack(side="left", padx=(0, 8))
        self.nameEntry = ctk.CTkEntry(
            actionFrame, placeholder_text="Enter reminder name", width=200
        )
        self.nameEntry.pack(side="left")
        self.nameEntry.insert(0, self.content["name"])
        
        # Delete Button
        DeleteButton(
            actionFrame,
            callback=lambda: ConfirmationMessage(
                "Are you sure you want to delete this reminder?",
                callback=self.delete_reminder,
            ),
            tooltipText="Delete Reminder",
        ).pack(side="right")

        # Time Frame
        timeFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        timeFrame.pack(padx=20, pady=(0, 10), fill="x")

        # Time Up Buttons
        TimeButton(
            timeFrame,
            upButton=True,
            callback=lambda: self.time_up("hour"),
            tooltipText="Hour Up",
        ).grid(row=0, column=0, sticky="nwse")
        TimeButton(
            timeFrame,
            upButton=True,
            callback=lambda: self.time_up("minute"),
            tooltipText="Minute Up",
        ).grid(row=0, column=2, sticky="nwse")
        TimeButton(
            timeFrame,
            upButton=True,
            callback=lambda: self.time_up("meridiem"),
            tooltipText="Meridiem Up",
        ).grid(row=0, column=3, sticky="nwse")

        # Time Entry
        self.hourEntry = ctk.CTkEntry(
            timeFrame, font=("Segoe UI", 16), width=40, height=36, justify="center"
        )
        self.hourEntry.grid(row=1, column=0, sticky="nwse")
        ctk.CTkLabel(timeFrame, text=":", font=("Segoe UI", 18, "bold")).grid(
            row=1, column=1, sticky="nwse", padx=5
        )
        self.minuteEntry = ctk.CTkEntry(
            timeFrame, font=("Segoe UI", 16), width=40, justify="center"
        )
        self.minuteEntry.grid(row=1, column=2, sticky="nwse")
        self.meridiemEntry = ctk.CTkEntry(
            timeFrame,
            font=("Segoe UI", 16),
            width=40,
            justify="center",
            state="readonly",
        )
        self.meridiemEntry._entry.configure(cursor="arrow")
        self.meridiemEntry.grid(row=1, column=3, sticky="nwse", padx=15)

        self.hourEntry.insert(0, self.content["time"].split(":")[0])
        self.minuteEntry.insert(0, self.content["time"].split(":")[1])
        self.set_meridiem(self.content["time"].split(":")[2])

        self.hourEntry.bind("<KeyRelease>", lambda event: self._unfocused(event, "hour"))
        self.minuteEntry.bind("<KeyRelease>", lambda event: self._unfocused(event, "minute"))
        self.hourEntry.bind("<FocusOut>", self._unfocused_format)
        self.minuteEntry.bind("<FocusOut>", self._unfocused_format)

        # Time Down Button
        TimeButton(
            timeFrame,
            upButton=False,
            callback=lambda: self.time_down("hour"),
            tooltipText="Hour Down",
        ).grid(row=2, column=0, sticky="nwse")
        TimeButton(
            timeFrame,
            upButton=False,
            callback=lambda: self.time_down("minute"),
            tooltipText="Minute Down",
        ).grid(row=2, column=2, sticky="nwse")
        TimeButton(
            timeFrame,
            upButton=False,
            callback=lambda: self.time_down("meridiem"),
            tooltipText="Meridiem Down",
        ).grid(row=2, column=3, sticky="nwse")

        # Date Picker
        reminderDate = get_datetime_from_string(
            self.content["date"], self.content["time"]
        )
        self.datePicker = Calendar(
            self.contentFrame,
            selectmode="day",
            day=reminderDate.day,
            month=reminderDate.month,
            year=reminderDate.year,
        )
        self.datePicker.pack(padx=25, pady=(0, 20), anchor="w")

        # Recurring Switch
        self.recurringSwitch = ctk.CTkSwitch(
            self.contentFrame,
            text="Recurring",
            command=self.toggle_recurring,
        )
        self.recurringSwitch.pack(padx=20, pady=(20, 5), anchor="w")
        if self.content["isRecurring"]:
            self.recurringSwitch.select()

        # Recurring Frame
        self.recurringFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )

        # Recurring Label
        ctk.CTkLabel(
            self.recurringFrame,
            text="Repeat every:",
            text_color="black",
            font=("Roboto", 13),
            anchor="w",
        ).pack(padx=(0, 8), side="left")

        # Recurring Number Entry
        self.recurringEntry = ctk.CTkEntry(
            self.recurringFrame,
            justify="center",
        )

        # Recurring Option
        self.recurringCombo = ctk.CTkComboBox(
            self.recurringFrame,
            values=["days", "weeks", "months", "years"],
            width=85,
            command=self.recurring_changed,
        )
        self.recurringCombo.set("days")

        self.recurringCombo.pack(side="right", padx=(8, 0))
        self.recurringEntry.pack(side="right", fill="x", expand=True)

        self.recurringEntry.insert(0, self.content["recurringNumber"])
        self.recurringCombo.set(self.content["recurringType"])

        # Save Button
        self.saveButton = SaveButton(
            self.contentFrame,
            self.save_changes,
            self.is_changed,
        )
        self.saveButton.pack(padx=20, pady=20, anchor="w")

        self.saveButton.update_state()

        # Setup UI
        self.toggle_recurring()

        # Events to trigger check if any changes
        self.nameEntry.bind(
            "<KeyRelease>", lambda event: self.saveButton.update_state()
        )
        self.hourEntry.bind(
            "<KeyRelease>", lambda event: self.saveButton.update_state()
        )
        self.minuteEntry.bind(
            "<KeyRelease>", lambda event: self.saveButton.update_state()
        )
        self.meridiemEntry.bind(
            "<KeyRelease>", lambda event: self.saveButton.update_state()
        )
        self.datePicker.bind(
            "<<CalendarSelected>>", lambda event: self.saveButton.update_state()
        )
        self.recurringEntry.bind(
            "<KeyRelease>", lambda event: self.saveButton.update_state()
        )

    def toggle_active(self):
        self.saveButton.update_state()

    def delete_reminder(self):
        ReminderController.delete_reminder(self.id)
        Global.pageManagers[Global.activeTab].back()

    def toggle_recurring(self):
        if self.recurringSwitch.get():
            self.recurringFrame.pack(
                padx=20, pady=10, fill="x", after=self.recurringSwitch
            )
        else:
            self.recurringFrame.pack_forget()

        self.saveButton.update_state()

    def recurring_changed(self, option):
        print("Recurring Changed", option)
        self.saveButton.update_state()

    def save_changes(self):
        name = self.nameEntry.get()
        isActive=self.activateReminderSwitch.get() == 1
        time = f"{self.hourEntry.get()}:{self.minuteEntry.get()}:{self.meridiemEntry.get()}"
        date = self.datePicker.selection_get().strftime("%Y-%m-%d")
        isRecurring = self.recurringSwitch.get() == 1
        recurringNumber = self.recurringEntry.get()
        recurringType = self.recurringCombo.get()

        if self.isNew:
            returnValue = ReminderController.create_reminder(
                self.listId,
                name,
                isActive,
                time,
                date,
                isRecurring,
                recurringNumber,
                recurringType
            )
        else:
            returnValue = ReminderController.edit_reminder(
            self.content["id"],
            name,
            isActive,
            time,
            date,
            isRecurring,
            recurringNumber,
            recurringType,
        )
        
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        if self.isNew:
            Notification.schedule(returnValue)
            self.id=returnValue["id"]
            self.isNew=False
        else:
            Notification.reschedule(returnValue)

        Global.pageManagers[Global.activeTab].back()


    def is_changed(self):

        if self.isNew:
            return True

        name = self.nameEntry.get()
        isActive=self.activateReminderSwitch.get()==1
        hour = self.hourEntry.get()
        minute = self.minuteEntry.get()
        meridiem = self.meridiemEntry.get()

        try:
            time = get_time_from_string(hour, minute, meridiem)
        except (ValueError, TypeError):
            return True

        date = self.datePicker.selection_get().strftime("%Y-%m-%d")

        isRecurring = self.recurringSwitch.get() == 1
        recurringNumber = self.recurringEntry.get()
        recurringType = self.recurringCombo.get()

        return (
            name != self.content["name"]
            or isActive != self.content["isActive"]
            or time != get_datetime_from_string(time_str=self.content["time"])
            or date != self.content["date"]
            or isRecurring != self.content["isRecurring"]
            or (isRecurring and recurringNumber != str(self.content["recurringNumber"]))
            or (isRecurring and recurringType != self.content["recurringType"])
        )

    def set_meridiem(self, value):
        self.meridiemEntry.configure(state="normal")
        self.meridiemEntry.delete(0, "end")
        self.meridiemEntry.insert(0, value)
        self.meridiemEntry.configure(state="readonly")

    def notification_end_callback(self, id):
        pass

    def _unfocused(self, event, timeType):
        widget = event.widget
        currentNum = widget.get()
        inputPosition = widget.index(ctk.INSERT)
        numValid="".join(filter(str.isdigit, currentNum))[:2]
        if numValid:
            num=int(numValid)
            if timeType=="hour":
                if num>12: numValid="12"
                elif num==0: numValid=""
            elif timeType=="minute":
                if num>59: numValid="59"
        if currentNum != numValid:
            widget.delete(0, 'end')
            widget.insert(0, numValid)
            widget.icursor(min(inputPosition, len(currentNum)))
        self.saveButton.update_state()

    def _unfocused_format(self, event):
        widget = event.widget
        currentNum = widget.get()

        if not currentNum:
            default="12" if widget == self.hourEntry else "00"
            widget.insert(0, default)
        elif len(currentNum) == 1:
            formattedNum = "0"+currentNum
            widget.delete(0, 'end')
            widget.insert(0, formattedNum)
        self.saveButton.update_state()

    def update_hour(self, change):
        try:
            current = int(self.hourEntry.get())
            new = current + change
            if new > 12: new = 1
            elif new < 1: new = 12
            self.hourEntry.delete(0, 'end')
            self.hourEntry.insert(0, f"{new:02d}")
        except ValueError:
            self.hourEntry.delete(0, 'end')
            self.hourEntry.insert(0, "12")
    
    def update_minute(self, change):
        try:
            current = int(self.minuteEntry.get())
            new = current + change
            if new > 59:
                new = 0
            elif new < 0:
                new = 59
            self.minuteEntry.delete(0, 'end')
            self.minuteEntry.insert(0, f"{new:02d}")
        except ValueError:
            self.minuteEntry.delete(0, 'end')
            self.minuteEntry.insert(0, "00")

    def time_up(self, timeType):
        if timeType == "hour": self.update_hour(1)
        elif timeType == "minute": self.update_minute(1)
        elif timeType == "meridiem": self.set_meridiem("PM" if self.meridiemEntry.get() == "AM" else "AM")
        self.saveButton.update_state()

    def time_down(self, timeType):
        if timeType == "hour": self.update_hour(-1)
        elif timeType == "minute": self.update_minute(-1)
        elif timeType == "meridiem": self.set_meridiem("PM" if self.meridiemEntry.get() == "AM" else "AM")
        self.saveButton.update_state()
    
