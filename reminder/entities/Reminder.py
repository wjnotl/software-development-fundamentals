from datetime import datetime

from utils.processing.DatetimeProcessing import is_datetime_expired, add_date_delta


class Reminder:
    def __init__(
        self,
        id,
        name,
        isActive,
        time,
        date,
        isRecurring,
        recurringNumber,
        recurringType,
        list,
    ):
        self.__id = id
        self.__name = name
        self.__isActive = isActive
        self.__time = time
        self.__date = date
        self.__isRecurring = isRecurring
        self.__recurringNumber = recurringNumber
        self.__recurringType = recurringType
        self.__list = list

    # Getter
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_isActive(self):
        return self.__isActive

    def get_time(self):
        return self.__time

    def get_date(self):
        return self.__date

    def get_isRecurring(self):
        return self.__isRecurring

    def get_recurringNumber(self):
        return self.__recurringNumber

    def get_recurringType(self):
        return self.__recurringType

    def get_list(self):
        return self.__list

    # Setter
    def set_name(self, name):
        self.__name = name

    def set_isActive(self, isActive):
        self.__isActive = isActive

    def set_time(self, time):
        self.__time = time

    def set_date(self, date):
        self.__date = date

    def set_isRecurring(self, isRecurring):
        self.__isRecurring = isRecurring

    def set_recurringNumber(self, recurringNumber):
        self.__recurringNumber = recurringNumber

    def set_recurringType(self, recurringType):
        self.__recurringType = recurringType

    def set_list(self, list):
        self.__list = list

    # Method
    def get_public_data(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "isActive": self.__isActive,
            "time": self.__time,
            "date": self.__date,
            "isRecurring": self.__isRecurring,
            "recurringNumber": self.__recurringNumber,
            "recurringType": self.__recurringType,
            "nextDate": self.get_next_date().strftime("%Y-%m-%d"),
            "listId": self.__list,
        }

    def get_next_date(self):
        date=datetime.strptime(self.__date, "%Y-%m-%d")
        if not self.__isRecurring:
            return date

        if not is_datetime_expired(self.__date, self.__time):
            return date

        newDate = add_date_delta(
            date,
            self.__recurringType,
            self.__recurringNumber,
        )

        while is_datetime_expired(newDate.strftime("%Y-%m-%d"), self.__time):
            newDate = add_date_delta(
                newDate, self.__recurringType, self.__recurringNumber
            )

        return newDate

    # Equal
    def __eq__(self, other):
        return isinstance(other, Reminder) and self.get_id() == other.get_id()
