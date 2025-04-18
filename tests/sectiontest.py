from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from collections.abc import Iterable
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
        self.assertIsNone(result)

    def test_assign_instructor_none(self):
        self.section.assign_instructor(None)
        self.assertIsNone(self.section.instructor)

    def test_assign_instructor_invalid(self):
        result = self.section.assign_instructor("not a user")
        self.assertIsNone(result)
        self.assertIsNone(self.section.instructor)

    # --- assign_assistants ---
    def test_assign_assistants_single_user(self):
        self.section.assign_assistants(self.user1)
        self.assertIn(self.user1, self.section.assistants.all())
        self.assertEqual(self.section.assistants.count(), 1)

    def test_assign_assistants_list_of_users(self):
        self.section.assign_assistants([self.user1, self.user2])
        self.assertIn(self.user1, self.section.assistants.all())
        self.assertIn(self.user2, self.section.assistants.all())
        self.assertEqual(self.section.assistants.count(), 2)

    def test_assign_assistants_queryset(self):
        users = User.objects.filter(username__in=['user1', 'user2'])
        self.section.assign_assistants(users)
        self.assertEqual(set(self.section.assistants.all()), set(users))

    def test_assign_assistants_invalid_type(self):
        result = self.section.assign_assistants("not a user")
        self.assertIsNone(result)
        self.assertEqual(self.section.assistants.count(), 0)

    def test_assign_assistants_list_with_invalid_element(self):
        # This will not raise but will set whatever is valid
        result = self.section.assign_assistants([self.user1, "not a user"])
        # Only the valid user will be set
        self.assertIn(self.user1, self.section.assistants.all())
        self.assertEqual(self.section.assistants.count(), 1)

    # --- set_schedule ---
    def test_set_schedule_valid(self):
        schedule = {"day": "Monday", "time": "09:00"}
        result = self.section.set_schedule(schedule)
        self.assertEqual(self.section.schedule, schedule)
        self.assertIsNone(result)

    def test_set_schedule_invalid(self):
        result = self.section.set_schedule("not a dict")
        self.assertIsNone(result)
        # Should remain unchanged (default is {})
        self.assertEqual(self.section.schedule, {})

    # --- unique_together constraint ---
    def test_unique_together_constraint(self):
        Section.objects.create(course=self.course, name="Section B")
        with self.assertRaises(IntegrityError):
            Section.objects.create(course=self.course, name="Section B")
