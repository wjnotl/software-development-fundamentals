from gpa.data.ProgrammeData import ProgrammeData
from gpa.data.SemesterData import SemesterData
from gpa.entities.Coursework import Coursework

from gpa.data.CourseworkData import CourseworkData
from gpa.data.CourseData import CourseData


class CourseworkController:
    # Getter
    def get_courseworks_by_course(courseId):
        course = CourseData.get_course_by_id(courseId)
        if course is None:
            return []

        data = []
        for coursework in course.get_courseworks():
            data.append(coursework.get_public_data())

    def get_coursework_public_data(id):
        coursework = CourseworkData.get_coursework_by_id(id)
        if coursework is None:
            return None

        return coursework.get_public_data()

    # Create
    def create_coursework(courseId):
        course = CourseData.get_course_by_id(courseId)
        if course is None:
            return "Course not found"

        coursework = Coursework(
            id=CourseworkController.__next_id(),
            name="Untitled Coursework",
            weight=0,
            score=0,
            course=course,
        )

        course.add_coursework(coursework)
        CourseworkData.add_coursework(coursework)

        error = CourseworkData.save()
        if error:
            return error

        return coursework.get_public_data()

    # Delete
    def delete_coursework(courseworkId):
        coursework = CourseworkData.get_coursework_by_id(courseworkId)
        if coursework is None:
            return "Coursework not found"
        course = coursework.get_course()

        # delete coursework
        course.remove_coursework(coursework)
        CourseworkData.delete_coursework(coursework)

        error = CourseworkData.save()
        if error:
            return error

        return None

    # Edit
    def edit_coursework(id, name, weight, score):
        coursework = CourseworkData.get_coursework_by_id(id)
        if coursework is None:
            return "Coursework not found"

        name = name.strip()
        error = CourseworkController.__is_name_valid(name)
        if error:
            return error

        error = CourseworkController.__is_weight_valid(weight)
        if error:
            return error

        error = CourseworkController.__is_score_valid(score)
        if error:
            return error

        coursework.set_name(name)
        coursework.set_weight(float(weight))
        coursework.set_score(float(score))

        error = CourseworkData.save()
        if error:
            return error

        return coursework.get_public_data()

    # Utils
    def __next_id():
        if len(CourseworkData.get_courseworks()) == 0:
            return 1

        return (
            max(coursework.get_id() for coursework in CourseworkData.get_courseworks())
            + 1
        )

    # Validation
    def __is_name_valid(name):
        if name == "":
            return "Name cannot be empty"

        if len(name) > 50:
            return "Name cannot be longer than 50 characters"

        return None

    def __is_weight_valid(weight):
        try:
            weight = float(weight)
            if weight < 0 or weight > 100:
                return "Weight must be between 0 and 100"
        except ValueError:
            return "Weight must be a number"
        return None

    def __is_score_valid(score):
        try:
            score = float(score)
            if score < 0 or score > 100:
                return "Score must be between 0 and 100"
        except ValueError:
            return "Score must be a number"

        return None
