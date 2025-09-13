class Semester:
    def __init__(self, id, name, programme):
        self.__id = id
        self.__name = name
        self.__programme = programme

        self.__courses = []

    # Getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_programme(self):
        return self.__programme

    def get_courses(self):
        return tuple(self.__courses)

    def get_public_data(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "gpa": self.calculate_gpa(),
            "credits": self.calculate_credit(),
        }

    # Setters
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_programme(self, programme):
        self.__programme = programme

    # Methods
    def add_course(self, course):
        self.__courses.append(course)

    def remove_course(self, course):
        for course in self.__courses:
            if course == course:
                self.__courses.remove(course)
                break

    def calculate_gpa(self):
        points = 0.0
        credit_hours = 0.0

        for course in self.__courses:
            credit = course.get_credit_hours()

            if course.get_grade() != "":
                points += course.get_grade_point() * credit  # Add weighted grade points
                credit_hours += credit

        # Avoid division by zero if no courses have result yet
        if credit_hours == 0:
            return 0

        return round(points / credit_hours, 4)

    def calculate_credit(self):
        return sum(course.get_credit_hours() for course in self.__courses if course.get_grade() != "F")

    # Equal
    def __eq__(self, other):
        return isinstance(other, Semester) and self.get_id() == other.get_id()
