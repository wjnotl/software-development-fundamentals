from reminder.controllers.ReminderController import ReminderController
import utils.core.Global as Global
from utils.core.Page import Page
from utils.ui.BackButton import BackButton
from utils.ui.DeleteButton import DeleteButton
from utils.ui.Message import ConfirmationMessage, ErrorMessage
from reminder.ui.Header import Header
import customtkinter as ctk

from reminder.ui.ReminderContainer import ReminderContainer

from utils.processing.DatetimeProcessing import is_datetime_expired

from reminder.controllers.ListController import ListController
from utils.ui.SaveButton import SaveButton


class ListPage(Page):
    def __init__(self, parentFrame, id):
        super().__init__(parentFrame)
        self.id = id

    def load_data(self):
        self.content = ListController.get_list_public_data(self.id)

        if self.content is None:
            ErrorMessage("List not found")
            return False

        self.reminders = ListController.get_reminders_by_list(self.id)

    def create_UI(self):
        self.header = Header(self._frame, self.content["name"])

        self.contentFrame = ctk.CTkScrollableFrame(
            self._frame, fg_color="transparent", corner_radius=0
        )
        self.contentFrame.pack(fill="both", expand=True)

        # Back Button
        BackButton(self.contentFrame).pack(pady=10, anchor="w")

        # Action Frame
        actionFrame = ctk.CTkFrame(
            self.contentFrame, corner_radius=0, fg_color="transparent"
        )
        actionFrame.pack(fill="x", padx=10, pady=10)

        # Name
        ctk.CTkLabel(
            actionFrame,
            text="Name:",
            text_color="black",
            font=("Segoe UI", 13),
            anchor="w",
        ).pack(side="left", padx=(0, 8))
        self.nameEntry = ctk.CTkEntry(
            actionFrame, placeholder_text="Enter list name", width=200
        )
        self.nameEntry.pack(side="left")
        self.nameEntry.insert(0, self.content["name"])

        # Delete Button
        DeleteButton(
            actionFrame,
            callback=lambda: ConfirmationMessage(
                "Are you sure you want to delete this list?",
                callback=self.delete_list,
            ),
            tooltipText="Delete List",
        ).pack(side="right")

        # Reminders
        self.reminderElements = []

        for reminder in self.reminders:
            container = ReminderContainer(
                self.contentFrame,
                reminder["name"],
                activeState=reminder["isActive"],
                dayText=reminder["date"],
                timeText=reminder["time"],
                recurring=reminder["isRecurring"],
                finished=is_datetime_expired(reminder["date"], reminder["time"]) and not reminder["isRecurring"],
                callback=lambda remId=reminder["id"]: self.navigate_to_reminder(remId),
            )
            container.id = reminder["id"]
            container.toggleActiveCallback=self.handle_reminder_toggle
            self.reminderElements.append(container)

        # Add Reminder Button
        ReminderContainer(
            self.contentFrame,
            addButton=True,
            tooltipText="Add new reminder",
            callback=self.add_reminder,
        )

        # Save Button
        self.saveButton = SaveButton(
            self.contentFrame,
            self.save_changes,
            self.is_changed,
        )
        self.saveButton.pack(padx=10, pady=30, anchor="w")

        self.nameEntry.bind(
            "<KeyRelease>", lambda event: self.saveButton.update_state()
        )

    def add_reminder(self):
        self.navigate_to_reminder(-1)

    def navigate_to_reminder(self, id):
        from reminder.pages.ReminderPage import ReminderPage

        Global.pageManagers["reminder"].show_page(ReminderPage, id, listId=self.id)

    def delete_list(self):
        ListController.delete_list(self.content["id"])        
        Global.pageManagers[Global.activeTab].back()
        
    def save_changes(self):
        returnValue = ListController.edit_list(self.content["id"], self.nameEntry.get())

        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        Global.pageManagers["reminder"].currentPage.refresh_frame()

    def is_changed(self):
        return self.nameEntry.get() != self.content["name"]

    def notification_end_callback(self, id):
        for index, reminder_data in enumerate(self.reminders):
            if reminder_data["id"] == id:
                rem = self.reminderElements[index]

                returnValue = ReminderController.get_reminder_public_data(id)
                if returnValue is None or isinstance(returnValue, str):
                    self.refresh_frame()
                    return

                self.reminders[index] = returnValue

                rem.update_date_label(returnValue["date"])

                rem.activeState = returnValue["isActive"]
                rem.update_bell_icon()

                if (
                    is_datetime_expired(returnValue["date"], returnValue["time"])
                    and not returnValue["isRecurring"]
                ):
                    rem.update_finished(True)

                break

    def handle_reminder_toggle(self, id):
        returnValue = ReminderController.toggle_active(id)
        if isinstance(returnValue, str):
            ErrorMessage(returnValue)
            return

        for container in self.reminderElements:
            if hasattr(container, 'id') and container.id == id:
                container.activeState = returnValue["isActive"]
                container.update_bell_icon()
                break