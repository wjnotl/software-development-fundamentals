from reminder.entities.List import List
from reminder.data.ListData import ListData
from reminder.data.ReminderData import ReminderData

class ListController:
    # Getter
    def get_reminders_by_list(listId):
        list = ListData.get_list_by_id(listId)
        if list is None:
            return []

        data = []
        for rem in list.get_reminders():
            data.append(rem.get_public_data())

        return data

    def get_list_public_data(id):
        list = ListData.get_list_by_id(id)
        if list is None:
            return None

        return list.get_public_data()

    def get_home_lists():
        data = []
        for list in ListData.get_lists():
            data.append(list.get_public_data())

        return data

    # Create
    def create_list():
        list = List(ListController.__next_id(), f"Untitled List {ListController.__next_id()}")

        ListData.add_list(list)

        error = ListData.save()
        if error:
            return error

        return list.get_public_data()

    # Delete
    def delete_list(listId):
        listToDelete = ListData.get_list_by_id(listId)
        if listToDelete is None:
            return "List not found"
        
        for reminder in listToDelete.get_reminders():
            ReminderData.remove_reminder(reminder)
        
        ListData.remove_list(listToDelete)
        error = ReminderData.save()
        if error:
            return error
        
        error = ListData.save()
        if error:
            return error
        
        return "List deleted"
    

    # Edit
    def edit_list(listId, name):
        list = ListData.get_list_by_id(listId)
        if list is None:
            return "List not found"

        name = name.strip()
        error = ListController.__is_name_valid(name)
        if error:
            return error

        list.set_name(name)

        error = ListData.save()
        if error:
            return error

        return list.get_public_data()

    # Utils
    def __next_id():
        if not ListData.get_lists():
            return 1

        return max([list.get_id() for list in ListData.get_lists()]) + 1

    # Validation
    def __is_name_valid(name):
        if name == "":
            return "Name cannot be empty"

        if len(name) > 50:
            return "Name cannot be longer than 50 characters"

        return None
