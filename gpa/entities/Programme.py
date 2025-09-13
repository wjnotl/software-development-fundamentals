class Programme:
    def __init__(self, id, name, grade_info):
        self.__id = id
        self.__name = name
        self.__grade_info = grade_info

        self.__semesters = []

    # Getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_semesters(self):
        return tuple(self.__semesters)

    def get_grade_info(self):
        return self.__grade_info

    def get_public_data(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "grade_info": self.get_grade_info(),
            "cgpa": self.calculate_cgpa(),
            "total_credit": self.calculate_total_credit(),
        }

    # Setters
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_grade_info(self, grade_info):
        self.__grade_info = grade_info

    # Methods
    def add_semester(self, semester):
        self.__semesters.append(semester)

    def remove_semester(self, semester):
        for sem in self.__semesters:
            if sem == semester:
                self.__semesters.remove(sem)
                break

    # def calculate_cgpa(self):
    #     total_points = 0.0
    #     total_credits = 0

    #     for semester in self.__semesters:
    #         for course in semester.get_courses():
    #             credit = course.get_credit_hours()

    #             if course.get_grade() != "" and course.get_grade() != "F":
    #                 total_points += (
    #                     course.get_grade_point() * credit
    #                 )  # Add weighted grade points
    #                 total_credits += credit

    #     if total_credits == 0:
    #         return 0.0

    #     return round((total_points / total_credits), 4)

    def calculate_cgpa(self):
        total_points = 0.0
        total_credits = 0
        latest_courses = {}

        for semester in self.__semesters:
            for course in semester.get_courses():
                if course.get_grade() != "":
                    current_course = latest_courses.get(course.get_name(), "")
                    if current_course == "":
                        latest_courses[course.get_name()] = course
                    elif course.get_grade_point() > current_course.get_grade_point():
                        latest_courses[course.get_name()] = course

        for course in latest_courses.values():
            credit = course.get_credit_hours()
            if course.get_grade() != "":
                total_points += course.get_grade_point() * credit  # Add weighted grade points
                total_credits += credit

        if total_credits == 0:
            return 0.0

        return round((total_points / total_credits),4)

    def calculate_total_credit(self):
        return sum(semester.calculate_credit() for semester in self.__semesters)

    # Equal
    def __eq__(self, other):
        return isinstance(other, Programme) and self.get_id() == other.get_id()
