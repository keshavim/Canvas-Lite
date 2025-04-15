import unittest

from core.courses import Course

# constructor tests
class TestInit(unittest.TestCase):
    # test default parameters (only course_id and title)
    def test_default(self):
        course = Course(1, "title")
        self.assertEqual(course.course_id, 1)
        self.assertEqual(course.title, "title")
        self.assertEqual(course.semester, "Fall")
        self.assertEqual(course.instructor_id, 0)

    # test default instructor_id (course_id, title, semester)
    def test_default_instructor(self):
        course = Course(1, "title", semester="Spring")
        self.assertEqual(course.course_id, 1)
        self.assertEqual(course.title, "title")
        self.assertEqual(course.semester, "Spring")
        self.assertEqual(course.instructor_id, 0)

    #test default semester (course_id, title, instructor_id)
    def test_default_semester(self):
        course = Course(1, "title", instructor_id=1)
        self.assertEqual(course.course_id, 1)
        self.assertEqual(course.title, "title")
        self.assertEqual(course.semester, "Fall")
        self.assertEqual(course.instructor_id, 1)

    # test proper initialization for each parameter filled in
    def test_full(self):
        course = Course(1, "title", "Spring", 1)
        self.assertEqual(course.course_id, 1)
        self.assertEqual(course.title, "title")
        self.assertEqual(course.semester, "Spring")
        self.assertEqual(course.instructor_id, 1)

    # test an invalid course_id (String), should raise TypeError
    def test_invalid_course_id(self):
        with self.assertRaises(TypeError, msg="Passing a String to the constructor (course_id) fails to raise TypeError"):
            course = Course("h", "title", "Spring", 1)

    # test invalid semester, should raise ValueError
    def test_invalid_semester(self):
        with self.assertRaises(ValueError, msg="Passing something aside from Fall/Spring to the constructor (semester) fails to raise ValueError"):
            course = Course(1, "title", "Autumn", 1)

    # test an invalid instructor_id (String), should raise TypeError
    def test_invalid_instructor_id(self):
        with self.assertRaises(TypeError, msg="Passing a String to the constructor (course_id) fails to raise TypeError"):
            course = Course(1, "title", "Spring", "h")

# test built-in String method
class TestString(unittest.TestCase):
    # test deleted course (values are None), should raise ValueError
    def test_deleted_string(self):
        with self.assertRaises(ValueError, msg="Attempting to convert a deleted course fails to raise TypeError"):
            course = Course(None, None, None, None)

    # test String for default course
    def test_default_string(self):
        course = Course(1, "title")
        self.assertEqual(course.__str__(), "1 title Fall 0")

    # test String for default instructor_id
    def test_default_instructor_string(self):
        course = Course(1, "title", semester="Spring")
        self.assertEqual(course.__str__(), "1 title Spring 0")

    # test String for default semester
    def test_default_semester_string(self):
        course = Course(1, "title", instructor_id=1)
        self.assertEqual(course.__str__(), "1 title Fall 1")

    # test fully filled out course
    def test_full_string(self):
        course = Course(1, "title", "Spring", 1)
        self.assertEqual(course.__str__(), "1 title Spring 1")

# test delete method, should set all attributes to None
class TestDeleteCourse(unittest.TestCase):
    # attempt to delete an already deleted course, should raise ValueError
    def test_delete_deleted_course(self):
        course = Course(None, None, None, None)
        with self.assertRaises(TypeError, msg="Attempting to delete an already deleted course fails to raise TypeError"):
            course.delete_course()

    # delete a course, all values should be None
    def test_delete(self):
        course = Course(1, "title")
        course.delete_course()
        self.assertIsNone(course.course_id)
        self.assertIsNone(course.title)
        self.assertIsNone(course.semester)
        self.assertIsNone(course.instructor_id)

# test update_id
class TestUpdateID(unittest.TestCase):
    # attempt to update deleted course's course_id, should raise ValueError
    def test_update_deleted_course_id(self):
        course = Course(None, None, None, None)
        with self.assertRaises(ValueError, msg="Attempting to update course_id of deleted course fails to raise ValueError"):
            course.update_id(1)

    # test invalid argument for updating id, should raise TypeError
    def test_invalid_update_course_id(self):
        course = Course(1, "title")
        with self.assertRaises(TypeError, msg="Attempting to update_id with a String fails to raise TypeError"):
            course.update_id("h")

    # test update_id
    def test_update_course_id(self):
        course = Course(1, "title")
        course.update_id(2)
        self.assertEqual(course.course_id, 2)

# test update_title
class TestUpdateTitle(unittest.TestCase):
    # attempt to update a deleted course's title, should raise a ValueError
    def test_update_deleted_title(self):
        course = Course(None, None, None, None)
        with self.assertRaises(ValueError, msg="Attempting to update title of deleted course fails to raise ValueError"):
            course.update_title("title")

    # test update_title
    def test_update_title(self):
        course = Course(1, "title")
        course.update_title("h")
        self.assertEqual(course.title, "h")

# test update_semester
class TestUpdateSemester(unittest.TestCase):
    # attempt to update a deleted course's semester, should raise a ValueError
    def test_update_deleted_semester(self):
        course = Course(None, None, None, None)
        with self.assertRaises(ValueError, msg="Attempting to update semester of deleted course fails to raise ValueError"):
            course.update_semester("Fall")

    # test invalid input for updating a semester, should raise ValueError
    def test_update_invalid_semester(self):
        course = Course(1, "title")
        with self.assertRaises(ValueError, msg="Attempting to update a course with an invalid semester fails to raise ValueError"):
            course.update_semester("h")

    # test update_semester
    def test_update_semester(self):
        course = Course(1, "title")
        course.update_semester("Spring")
        self.assertEqual(course.semester, "Spring")

# test update_instructor
class TestUpdateInstructorID(unittest.TestCase):
    # attempt to update instructor_id for a deleted course, should raise ValueError
    def test_update_deleted_instructor_id(self):
        course = Course(None, None, None, None)
        with self.assertRaises(ValueError, msg="Attempting to update instructor ID of deleted course fails to raise ValueError"):
            course.update_instructor(1)

    # test invalid argument for updating instructor_id, should raise TypeError
    def test_invalid_update_instructor_id(self):
        course = Course(1, "title")
        with self.assertRaises(TypeError, msg="Attempting to update_instructor with a String fails to raise TypeError"):
            course.update_instructor("h")

    # test update_instructor
    def test_update_instructor_id(self):
        course = Course(1, "title")
        course.update_instructor(2)
        self.assertEqual(course.instructor_id, 2)