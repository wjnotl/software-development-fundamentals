from gpa.entities.Semester import Semester

from gpa.data.SemesterData import SemesterData
from gpa.data.ProgrammeData import ProgrammeData
from gpa.data.CourseData import CourseData
from gpa.data.CourseworkData import CourseworkData

class SemesterController:
    # Getter
    def get_courses_by_semester(semesterId):
        semester = SemesterData.get_semester_by_id(semesterId)
        if semester is None:
            return []

        data = []
        for course in semester.get_courses():
            data.append(course.get_public_data())

        return data

    def get_semester_public_data(id):
        semester = SemesterData.get_semester_by_id(id)
        if semester is None:
            return None

        return semester.get_public_data()
    
    def get_total_gpa(semester_id):
        semester = SemesterData.get_semester_by_id(semester_id)
        if semester is None:
            return 0
        return semester.calculate_gpa()
    
    def get_total_credit(semester_id):
        semester = SemesterData.get_semester_by_id(semester_id)  
        if semester is None:
            return 0
        return semester.calculate_credit()

    # Create
    def create_semester(programmeId):
        programme = ProgrammeData.get_programme_by_id(programmeId)
        if programme is None:
            return "Programme not found"

        semester = Semester(
            id=SemesterController.__next_id(),
            name="Untitled Semester",
            programme=programme,
        )

        programme.add_semester(semester)
        SemesterData.add_semester(semester)

        error = SemesterData.save()
        if error:
            return error

        return semester.get_public_data()

    # Delete
    def delete_semester(semesterId):
        semester =  SemesterData.get_semester_by_id(semesterId)
        if semester is None:
            return "Semester not found"

        programme = semester.get_programme()
        if programme is None:
            return "Programme not found"
        
        # delete coursework
        for course in semester.get_courses():
            for coursework in course.get_courseworks():
                CourseworkData.delete_coursework(coursework)
            CourseData.delete_course(course)

        # delete semester
        programme.remove_semester(semester)
        SemesterData.delete_semester(semester)

        error = CourseworkData.save()
        if error:
            return error

        error = CourseData.save()
        if error:
            return error

        error = SemesterData.save()
        if error:
            return error

        return None

    # Edit
    def edit_semester(id, name):
        semester = SemesterData.get_semester_by_id(id)
        if semester is None:
            return "Semester not found"

        name = name.strip()
        error = SemesterController.__is_name_valid(name)
        if error:
            return error

        semester.set_name(name)

        error = SemesterData.save()
        if error:
            return error

        return semester.get_public_data()

    # Utils
    def __next_id():
        if len(SemesterData.get_semesters()) == 0:
            return 1

        return max(semester.get_id() for semester in SemesterData.get_semesters()) + 1

    # Validation
    def __is_name_valid(name):
        if name == "":
            return "Name cannot be empty"

        if len(name) > 50:
            return "Name cannot be longer than 50 characters"

        return None
