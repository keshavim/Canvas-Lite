import unittest

class TestUserManager(unittest.TestCase):
    def test_register(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass


class TestUser(unittest.TestCase):
    def test_user_creation(self):
        pass

    def test_user_attributes(self):
        pass


class TestTA(unittest.TestCase):
    def test_ta_creation(self):
        pass

    def test_send_notification(self):
        pass


class TestInstructor(unittest.TestCase):
    def test_instructor_creation(self):
        pass

    def test_assign_course_to_ta(self):
        pass

    def test_assign_labsection_to_ta(self):
        pass


class TestAdmin(unittest.TestCase):
    def test_admin_creation(self):
        pass

    def test_create_course(self):
        pass

    def test_create_labsection(self):
        pass

    def test_delete_user(self):
        pass

    def test_delete_labsection(self):
        pass

    def test_delete_course(self):
        pass

    def test_assign_course_to_instructor(self):
        pass

    def test_assign_labsection_to_instructor(self):
        pass
