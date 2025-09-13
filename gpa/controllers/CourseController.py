from gpa.data.CourseworkData import CourseworkData
from gpa.data.ProgrammeData import ProgrammeData
from gpa.entities.Course import Course

from gpa.data.CourseData import CourseData
from gpa.data.SemesterData import SemesterData


class CourseController:
    # Getter
    def get_courseworks_by_course(courseId):
        course = CourseData.get_course_by_id(courseId)
        if course is None:
            return []

        data = []
        for coursework in course.get_courseworks():
            data.append(coursework.get_public_data())

        return data

    def get_course_public_data(id):
        course = CourseData.get_course_by_id(id)
        if course is None:
            return None

        return course.get_public_data()

    def get_coursework_score(id):
        course = CourseData.get_course_by_id(id)
        if not course:
            return 0
        return course.calculate_total_coursework_score()

    def get_predicted_grade_final_assessment_score(courseId):
        course = CourseData.get_course_by_id(courseId)
        if course is None:
            return "-"

        semester = course.get_semester()
        if semester is None:
            return "-"

        programme = semester.get_programme()
        if programme is None:
            return "-"

        return str(course.min_final_score()) + "%"

    def get_grade_point_from_grade(courseId, grade):
        course = CourseData.get_course_by_id(courseId)
        if course is None:
            return 0
        grade_info = course.get_semester().get_programme().get_grade_info()
        return grade_info.get(grade, [0])[0]

    # Create
    def create_course(semesterId):
        semester = SemesterData.get_semester_by_id(semesterId)
        if semester is None:
            return "Semester not found"

        course = Course(
            id=CourseController.__next_id(),
            name="Untitled Course",
            credit_hours=0,
            coursework_weight=0,
            has_final=True,
            desired_grade="A+",
            grade="-",
            semester=semester,
        )

        semester.add_course(course)
        CourseData.add_course(course)

        error = CourseData.save()
        if error:
            return error

        return course.get_public_data()

    # Delete
    def delete_course(courseId):
        course = CourseData.get_course_by_id(courseId)
        if course is None:
            return "Course not found"

        semester = course.get_semester()
        if semester is None:
            return "Semester not found"

        # delete courseswork
        for coursework in course.get_courseworks():
            CourseworkData.delete_coursework(coursework)

        # delete course
        semester.remove_course(course)
        CourseData.delete_course(course)

        error = CourseworkData.save()
        if error:
            return error

        error = CourseData.save()
        if error:
            return error

        return None

    # Edit
    def edit_course(
        id, name, coursework_weight, credit_hours, has_final, desired_grade, grade
    ):
        course = CourseData.get_course_by_id(id)
        if course is None:
            return "Course not found"

        name = name.strip()
        error = CourseController.__is_name_valid(name)
        if error:
            return error

        error = CourseController.__is_coursework_weight_valid(coursework_weight)
        if error:
            return error

        error = CourseController.__is_credit_hours_valid(credit_hours)
        if error:
            return error

        error = CourseController.__is_has_final_valid(has_final)
        if error:
            return error

        if has_final:
            error = CourseController.__is_desired_grade_valid(desired_grade)
            if error:
                return error
        else:
            desired_grade = "A+"

        error = CourseController.__is_grade_valid(grade)
        if error:
            return error

        course.set_name(name)
        course.set_coursework_weight(float(coursework_weight))
        course.set_credit_hours(int(credit_hours))
        course.set_has_final(has_final)
        course.set_desired_grade(desired_grade)
        course.set_grade(grade)

        error = CourseData.save()
        if error:
            return error

        return course.get_public_data()

    # Utils
    def __next_id():
        if len(CourseData.get_courses()) == 0:
            return 1

        return max(course.get_id() for course in CourseData.get_courses()) + 1

    # Validation
    def __is_name_valid(name):
        if name == "":
            return "Name cannot be empty"

        if len(name) > 50:
            return "Name cannot be longer than 50 characters"

        return None

    def __is_credit_hours_valid(hours):
        try:
            hours = int(hours)
            if hours < 0:
                return "Credit hours cannot be negative"
            
            if hours > 99:
                return "Credit hours cannot be greater than 99"

        except ValueError:
            return "Credit hours must be an integer"

        return None

    def __is_coursework_weight_valid(weight):
        try:
            weight = float(weight)
            if weight < 0 or weight > 100:
                return "Coursework weight must be between 0 and 100"

        except ValueError:
            return "Coursework weight must be a number"
        except:
            return "Unknown error"
        
        return None

    def __is_has_final_valid(has_final):
        if has_final not in [True, False]:
            return "Has final assessment must be either True or False"

        return None

    def __is_desired_grade_valid(grade):
        if grade not in [
            "A+",
            "A",
            "A-",
            "B+",
            "B",
            "B-",
            "C+",
            "C",
            "F",
        ]:
            return "Desired grade must be one of the following: A+, A, A-, B+, B, B-, C+, C, F"

        return None

    def __is_grade_valid(grade):
        if grade not in ["-", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F"]:
            return (
                "Grade must be one of the following: A+, A, A-, B+, B, B-, C+, C, F"
                or "-"
            )

        return None
