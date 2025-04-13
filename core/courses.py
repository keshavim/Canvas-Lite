
from BMIApp.models import Course
from django.core.exceptions import ObjectDoesNotExist

class CourseManager:
    """
    Manages course creation and instructor assignment.
    """

    def create_course(self, course_data):
        """
        Creates a new course.
        """
        return Course.objects.create(
            course_code=course_data.get("course_code"),
            title=course_data.get("title"),
            semester=course_data.get("semester"),
            instructor_id=course_data.get("instructor_id", None)
        )

    def assign_instructor(self, course_id, instructor_id):
        """
        Assigns an instructor to a course.
        """
        try:
            course = Course.objects.get(id=course_id)
            course.instructor_id = instructor_id
            course.save()
            return course
        except ObjectDoesNotExist:
            return None
