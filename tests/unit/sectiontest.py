from django.test import TestCase
from django.db import IntegrityError
from webapp.models import Course, Section, User

class SectionModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Math 101")
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.section = Section.objects.create(course=self.course, name="Section A")

    def test_str_representation(self):
        self.assertEqual(str(self.section), f"{self.course.name} - Section A")

    # --- assign_instructor ---
    def test_assign_instructor_valid(self):
        result = self.section.assign_instructor(self.user1)
        self.assertEqual(self.section.instructor, self.user1)
        self.assertTrue(result)

    def test_assign_instructor_none(self):
        result = self.section.assign_instructor(None)
        self.assertTrue(result)
        self.assertIsNone(self.section.instructor)

    def test_assign_instructor_invalid(self):
        result = self.section.assign_instructor("not a user")
        self.assertFalse(result)
        self.assertIsNone(self.section.instructor)

    # --- set_schedule ---
    def test_set_schedule_valid(self):
        schedule = {"day": "Monday", "time": "09:00"}
        result = self.section.set_schedule(schedule)
        self.assertEqual(self.section.schedule, schedule)
        self.assertTrue(result)

    def test_set_schedule_invalid(self):
        result = self.section.set_schedule("not a dict")
        self.assertFalse(result)
        # Should remain unchanged (default is {})
        self.assertEqual(self.section.schedule, {})

    # --- unique_together constraint ---
    def test_unique_together_constraint(self):
        Section.objects.create(course=self.course, name="Section B")
        with self.assertRaises(IntegrityError):
            Section.objects.create(course=self.course, name="Section B")
