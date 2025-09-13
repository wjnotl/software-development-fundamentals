class Coursework:
    def __init__(self, id, name, weight, score, course):
        self.__id = id
        self.__name = name
        self.__weight = weight
        self.__score = score
        self.__course = course

    # Getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_weight(self):
        return self.__weight

    def get_score(self):
        return self.__score
    
    def get_course(self):
        return self.__course
    
    def get_public_data(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "weight": self.get_weight(),
            "score": self.get_score(),
        }


    # Setters
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_weight(self, weight):
        self.__weight = weight

    def set_score(self, score):
        self.__score = score

    # Equal
    def __eq__(self, other):
        return isinstance(other, Coursework) and self.get_id() == other.get_id()