import math


class Course:
    def __init__(
        self,
        id,
        name,
        coursework_weight,
        credit_hours,
        has_final,
        desired_grade,
        grade,
        semester,
    ):
        self.__id = id
        self.__name = name
        self.__coursework_weight = coursework_weight
        self.__credit_hours = credit_hours
        self.__has_final = has_final
        self.__desired_grade = desired_grade
        self.__grade = grade
        self.__semester = semester

        self.__courseworks = []

    # Getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_credit_hours(self):
        return self.__credit_hours

    def get_coursework_weight(self):
        return self.__coursework_weight

    def get_has_final(self):
        return self.__has_final

    def get_desired_grade(self):
        return self.__desired_grade

    def get_grade(self):
        return self.__grade

    def get_semester(self):
        return self.__semester

    def get_courseworks(self):
        return tuple(self.__courseworks)

    def get_public_data(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "credit_hours": self.get_credit_hours(),
            "coursework_weight": self.get_coursework_weight(),
            "has_final": self.get_has_final(),
            "desired_grade": self.get_desired_grade(),
            "grade": self.get_grade(),
        }

    # Setters
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_credit_hours(self, credit_hours):
        self.__credit_hours = credit_hours

    def set_coursework_weight(self, weight):
        self.__coursework_weight = weight

    def set_has_final(self, has_final):
        self.__has_final = has_final

    def set_desired_grade(self, desired_grade):
        self.__desired_grade = desired_grade

    def set_grade(self, grade):
        self.__grade = grade

    def set_semester(self, semester):
        self.__semester = semester

    # Methods
    def add_coursework(self, coursework):
        self.__courseworks.append(coursework)

    def remove_coursework(self, coursework):
        for cw in self.__courseworks:
            if cw == coursework:
                self.__courseworks.remove(cw)
                break

    def calculate_total_coursework_score(self):
        total = 0
        for cw in self.__courseworks:
            score = cw.get_score() or 0   # handle None as 0
            weight = cw.get_weight() or 0 # handle None as 0
            total += score * (weight / 100)
        return round(total, 2)
    

    def min_final_score(self):
        grade_info = self.__semester.get_programme().get_grade_info()
        if self.__desired_grade not in grade_info:
            return "-"

        desired_score = grade_info[self.__desired_grade][1]
        final_weight = 100 - self.__coursework_weight

        courwork_score = self.calculate_total_coursework_score()
        target = desired_score - round(
            (courwork_score * self.__coursework_weight) /100
        )
        if final_weight <= 0:
            return "-"

        return math.ceil((target - 0.5) / final_weight * 100)


    def get_grade_point(self):
        if self.__grade in ("", "-"):
            return 0
        
        grade_info = self.__semester.get_programme().get_grade_info()
        return grade_info.get(self.__grade, [0])[0]  # safe lookup


    # Equal
    def __eq__(self, other):
        return isinstance(other, Course) and self.get_id() == other.get_id()
