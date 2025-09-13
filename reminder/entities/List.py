class List:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

        self.__reminders = []

    # Getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_reminders(self):
        return tuple(self.__reminders)

    def get_public_data(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
        }

    # Setters
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    # Method
    def add_reminder(self, reminder):
        self.__reminders.append(reminder)

    def remove_reminder(self, reminder):
        for r in self.__reminders:
            if r == reminder:
                self.__reminders.remove(r)
                break

    # Equal
    def __eq__(self, other):
        return isinstance(other, List) and self.get_id() == other.get_id()
