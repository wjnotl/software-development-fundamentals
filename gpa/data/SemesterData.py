import os
import csv

import utils.core.Global as Global

from gpa.entities.Semester import Semester

from gpa.data.ProgrammeData import ProgrammeData


class SemesterData:
    __semesters = []

    # Getter
    def get_semesters():
        return tuple(SemesterData.__semesters)

    def get_semester_by_id(id):
        for semester in SemesterData.__semesters:
            if semester.get_id() == id:
                return semester
        return None

    # Method
    def add_semester(semester):
        SemesterData.__semesters.append(semester)

    def delete_semester(semester):
        for s in SemesterData.__semesters:
            if s == semester:
                SemesterData.__semesters.remove(s)
                break

    # Storage
    def save():
        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "gpa", "storage", "semesters.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for semester in SemesterData.get_semesters():
                    data.append(
                        [
                            semester.get_id(),
                            semester.get_name(),
                            semester.get_programme().get_id(),
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
            path = os.path.join(Global.CURRENT_PATH, "gpa", "storage", "semesters.csv")
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass

            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        programme = ProgrammeData.get_programme_by_id(int(row[2]))
                        if programme:
                            semester = Semester(int(row[0]), row[1], programme)
                            programme.add_semester(semester)
                            SemesterData.__semesters.append(semester)
                    except:
                        errorMessage = "Some semesters data are corrupted"
                        continue

        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return errorMessage
