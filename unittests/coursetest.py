import unittest

from core.courses import CourseManager

class TestInit(unittest.TestCase):
    # test proper initialization
    def test_init(self):
        course = CourseManager(1, "title", "Spring 2024", 1)
        self.assertEqual(course.course_id, 1)
        self.assertEqual(course.title, "title")
        self.assertEqual(course.semester, "Spring 2024")
        self.assertEqual(course.instructor_id, 1)


class TestString(unittest.TestCase):
    pass

class TestCourseManager(unittest.TestCase):
    pass

class TestCreateCourse(unittest.TestCase):
    pass

class TestDeleteCourse(unittest.TestCase):
    pass

class TestGetCourse(unittest.TestCase):
    pass

class TestUpdateCourse(unittest.TestCase):
    pass