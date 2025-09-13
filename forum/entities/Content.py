class Content:
    def __init__(self, id, account, text, creationTime):
        self._id = id
        self._account = account
        self._text = text
        self._creationTime = creationTime

    # Getter
    def get_id(self):
        return self._id

    def get_account(self):
        return self._account

    def get_text(self):
        return self._text

    def get_creationTime(self):
        return self._creationTime

    def get_public_data(self):
        return {
            "id": self.get_id(),
            "account": (
                self.get_account().get_public_data() if self.get_account() else None
            ),
            "text": self.get_text(),
            "creationTime": self.get_creationTime(),
            "canReply": self.get_can_reply(),
        }
    
    # Setter
    def set_account(self, account):
        self._account = account

    # Equal
    def __eq__(self, other):
        return (isinstance(other, Content)) and self.get_id() == other.get_id()
