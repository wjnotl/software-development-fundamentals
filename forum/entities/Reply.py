from forum.entities.Content import Content


class Reply(Content):
    def __init__(self, id, account, text, creationTime, parentContent):
        super().__init__(id, account, text, creationTime)
        self.__parentContent = parentContent

    # Getters
    def get_parentContent(self):
        return self.__parentContent

    def get_public_data(self):
        data = super().get_public_data()
        data["parentContent"] = self.get_parentContent().get_public_data()
        return data

    def get_can_reply(self):
        """Check if the current reply can have sub replies"""
        return not isinstance(self.get_parentContent(), Reply)

    # Equal
    def __eq__(self, other):
        return isinstance(other, Reply) and self.get_id() == other.get_id()
