import os
import csv

import utils.core.Global as Global

from reminder.entities.List import List

class ListData:
    __lists = []

    # Getter
    def get_lists():
        return tuple(ListData.__lists)

    def get_list_by_id(id):
        for list_item in ListData.__lists:
            if list_item.get_id() == id:
                return list_item
        return None

    # Method
    def add_list(list_obj):
        ListData.__lists.append(list_obj)

    def remove_list(list_obj):
        for l in ListData.__lists:
            if l == list_obj:
                ListData.__lists.remove(l)
                break

    # Storage
    def save():
        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "reminder", "storage", "lists.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for list_item in ListData.get_lists():
                    data.append(
                        [
                            list_item.get_id(),
                            list_item.get_name(),
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
            path = os.path.join(Global.CURRENT_PATH, "reminder", "storage", "lists.csv")
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass
                return None
            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if not row:
                        continue
                    list_obj = List(int(row[0]), row[1]) 
                    ListData.add_list(list_obj)
        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return None
