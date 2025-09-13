import os
import csv
import json

import utils.core.Global as Global

from gpa.entities.Course import Course

from gpa.data.SemesterData import SemesterData


class CourseData:
    __courses = []

    # Getter
    def get_courses():
        return tuple(CourseData.__courses)

    def get_course_by_id(id):
        for course in CourseData.__courses:
            if course.get_id() == id:
                return course
        return None

    # Method
    def add_course(course):
        CourseData.__courses.append(course)

    def delete_course(course):
        for c in CourseData.__courses:
            if c == course:
                CourseData.__courses.remove(c)
                break

    # Storage
    def save():
        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "gpa", "storage", "courses.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for course in CourseData.get_courses():
                    data.append(
                        [
                            course.get_id(),
                            course.get_name(),
                            course.get_coursework_weight(),
                            course.get_credit_hours(),
                            course.get_has_final(),
                            course.get_desired_grade(),
                            course.get_grade(),
                            course.get_semester().get_id(),
                        ]
                    )
                writer.writerows(data)

        except PermissionError:
            return "Permission denied while saving the file"

        except IOError as e:
            return "IOError: " + str(e)

        return None

    def load():
        errorMessage = None

        try:
            path = os.path.join(Global.CURRENT_PATH, "gpa", "storage", "courses.csv")
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass

            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        semester = SemesterData.get_semester_by_id(int(row[7]))
                        if semester:
                            course = Course(
                                int(row[0]),        # id
                                row[1],             # name
                                float(row[2]),        # coursework_weight
                                int(row[3]),        # credit_hours
                                row[4].lower() == "true",  # has_final (bool)
                                row[5],             # desired_grade
                                row[6],             # grade
                                semester
                            )
                            semester.add_course(course)
                            CourseData.__courses.append(course)
                    except:
                        errorMessage = "Some courses data are corrupted"
                        continue

        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return errorMessage