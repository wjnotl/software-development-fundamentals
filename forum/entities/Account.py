import bcrypt


class Account:
    def __init__(self, id, username, passwordHash, token, name):
        self.__id = id
        self.__username = username
        self.__passwordHash = passwordHash
        self.__token = token
        self.__name = name

    # Getters
    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def get_passwordHash(self):
        return self.__passwordHash

    def get_token(self):
        return self.__token

    def get_name(self):
        return self.__name

    def get_public_data(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
        }

    def get_private_data(self):
        return {
            "id": self.get_id(),
            "token": self.get_token(),
            "name": self.get_name(),
        }

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_token(self, token):
        self.__token = token

    # Methods
    def is_password_correct(self, password):
        """Check if the given password matches the saved hash.
        :param password: The password to check.
        :return: True if matched, otherwise False.
        """

        return bcrypt.checkpw(password.encode(), self.__passwordHash.encode())

    # Equal
    def __eq__(self, other):
        return isinstance(other, Account) and self.get_id() == other.get_id()
