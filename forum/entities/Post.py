from forum.entities.Content import Content


class Post(Content):
    def __init__(self, id, account, text, creationTime, title):
        super().__init__(id, account, text, creationTime)
        self.__title = title

    # Getters
    def get_title(self):
        return self.__title

    def get_public_data(self):
        data = super().get_public_data()
        data["title"] = self.get_title()
        return data

    def get_can_reply(self):
        return True

    # Equal
    def __eq__(self, other):
        return isinstance(other, Post) and self.get_id() == other.get_id()
