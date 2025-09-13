import os
import csv

import utils.core.Global as Global

from gpa.entities.Coursework import Coursework
from gpa.data.CourseData import CourseData


class CourseworkData:
    __courseworks = []

    # Getter
    def get_courseworks():
        return tuple(CourseworkData.__courseworks)

    def get_coursework_by_id(id):
        for coursework in CourseworkData.__courseworks:
            if coursework.get_id() == id:
                return coursework
        return None

    # Method
    def add_coursework(coursework):
        CourseworkData.__courseworks.append(coursework)

    def delete_coursework(coursework):
        for cw in CourseworkData.__courseworks:
            if cw == coursework:
                CourseworkData.__courseworks.remove(cw)
                break

    # Storage
    def save():
        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "gpa", "storage", "courseworks.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for coursework in CourseworkData.__courseworks:
                    data.append(
                        [
                            coursework.get_id(),
                            coursework.get_name(),
                            coursework.get_weight(),
                            coursework.get_score(),
                            coursework.get_course().get_id(),
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
            path = os.path.join(Global.CURRENT_PATH, "gpa", "storage", "courseworks.csv")
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass

            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        course = CourseData.get_course_by_id(int(row[4]))
                        if course:
                            coursework = Coursework(
                                int(row[0]),     # id
                                row[1],          # name
                                float(row[2]),     # weight
                                float(row[3]),     # score
                                course           # course
                            )
                            course.add_coursework(coursework)
                            CourseworkData.__courseworks.append(coursework)
                    except:
                        errorMessage = "Some courseworks data are corrupted"
                        continue

        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return errorMessage