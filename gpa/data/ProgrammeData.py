import os
import csv
import json

import utils.core.Global as Global

from gpa.entities.Programme import Programme


class ProgrammeData:
    __programmes = []

    # Getter
    def get_programmes():
        return tuple(ProgrammeData.__programmes)

    def get_programme_by_id(id):
        for programme in ProgrammeData.__programmes:
            if programme.get_id() == id:
                return programme
        return None

    # Method
    def add_programme(programme):
        ProgrammeData.__programmes.append(programme)

    def delete_programme(programme):
        for p in ProgrammeData.__programmes:
            if p == programme:
                ProgrammeData.__programmes.remove(p)
                break

    # Storage
    def save():
        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "gpa", "storage", "programmes.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for programme in ProgrammeData.get_programmes():
                    data.append(
                        [
                            programme.get_id(),
                            programme.get_name(),
                            json.dumps(programme.get_grade_info()),
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
            path = os.path.join(Global.CURRENT_PATH, "gpa", "storage", "programmes.csv")
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass

            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        programme = Programme(int(row[0]), row[1], json.loads(row[2]))
                        ProgrammeData.__programmes.append(programme)
                    except:
                        errorMessage = "Some programmes data are corrupted"
                        continue

        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return errorMessage
