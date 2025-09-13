class Like:
    __likes = []

    def __init__(self, account, content):
        self.__account = account
        self.__content = content

        Like.__likes.append(self)

    # Getters
    def get_account(self):
        return self.__account

    def get_content(self):
        return self.__content

    def get_likes():
        return Like.__likes

    # Equal
    def __eq__(self, other):
        return (
            isinstance(other, Like)
            and self.get_account() == other.get_account()
            and self.get_content() == other.get_content()
        )
