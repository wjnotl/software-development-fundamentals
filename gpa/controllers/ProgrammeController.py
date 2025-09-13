from gpa.data.SemesterData import SemesterData
from gpa.entities.Programme import Programme
from gpa.data.ProgrammeData import ProgrammeData
from gpa.data.CourseData import CourseData
from gpa.data.CourseworkData import CourseworkData


class ProgrammeController:
    # Getter
    def get_semesters_by_programme(programmeId):
        programme = ProgrammeData.get_programme_by_id(programmeId)
        if programme is None:
            return []

        data = []
        for semester in programme.get_semesters():
            data.append(semester.get_public_data())

        return data

    def get_home_programmes():
        data = []
        for programme in ProgrammeData.get_programmes():
            data.append(programme.get_public_data())

        return data

    def get_programme_public_data(id):
        programme = ProgrammeData.get_programme_by_id(id)
        if programme is None:
            return None

        return programme.get_public_data()

    # Create
    def create_programme():
        programme = Programme(
            id=ProgrammeController.__next_id(),
            name="Untitled Programme",
            grade_info={
                "A+": [4.0, 90],
                "A": [4.0, 80],
                "A-": [3.67, 75],
                "B+": [3.33, 70],
                "B": [3.0, 65],
                "B-": [2.67, 60],
                "C+": [2.33, 55],
                "C": [2.0, 50],
                "F": [0.0, 0],
            },
        )

        ProgrammeData.add_programme(programme)

        error = ProgrammeData.save()
        if error:
            return error

        return programme.get_public_data()

    # Delete
    def delete_programme(programmeId):
        programme = ProgrammeData.get_programme_by_id(programmeId)
        if programme is None:
            return "Programme not found"

        # delete coursework
        for semester in programme.get_semesters():
            for course in semester.get_courses():
                for coursework in course.get_courseworks():
                    CourseworkData.delete_coursework(coursework)
                CourseData.delete_course(course)
            SemesterData.delete_semester(semester)

        # delete programme
        ProgrammeData.delete_programme(programme)

        error = CourseworkData.save()
        if error:
            return error

        error = CourseData.save()
        if error:
            return error

        error = SemesterData.save()
        if error:
            return error

        error = ProgrammeData.save()
        if error:
            return error

        return None

    # Edit
    def edit_programme(id, name, grade_info = None):
        programme = ProgrammeData.get_programme_by_id(id)
        if programme is None:
            return "Programme not found"

        name = name.strip()
        error = ProgrammeController.__is_name_valid(name)
        if error:
            return error

        if grade_info is not None:
            error = ProgrammeController.__is_grade_info_valid(grade_info)
            if error:
                return error

        programme.set_name(name)

        if grade_info is not None:
            for grade, value in grade_info.items():
                grade_info[grade][0] = float(value[0])
                grade_info[grade][1] = int(value[1])
            programme.set_grade_info(grade_info)

        error = ProgrammeData.save()
        if error:
            return error

        return programme.get_public_data()

    # Utils
    def __next_id():
        if len(ProgrammeData.get_programmes()) == 0:
            return 1

        return (
            max(programme.get_id() for programme in ProgrammeData.get_programmes()) + 1
        )

    # Validation
    def __is_name_valid(name):
        if name == "":
            return "Name cannot be empty"

        if len(name) > 50:
            return "Name cannot be longer than 50 characters"

        return None

    def __is_grade_info_valid(grade_info):
        for grade, value in grade_info.items():
            if value[0] is None:
                return "Points cannot be empty"

            if value[1] is None:
                return "Score cannot be empty"

            try:
                value[0] = float(value[0])
                if value[0] < 0 or value[0] > 4.0:
                    return "Points must be between 0 and 4.0"
            except ValueError:
                return "Points must be a number"
            except:
                return "Unknown error"

            try:
                value[1] = int(value[1])
                if value[1] < 0 or value[1] > 100:
                    return "Score must be between 0 and 100"
            except ValueError:
                return "Score must be an integer"
            except:
                return "Unknown error"

        return None
