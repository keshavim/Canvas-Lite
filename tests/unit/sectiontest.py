from django.test import TestCase
from django.db import IntegrityError
from webapp.models import Course, User, Section
from webapp.models.section import SectionType


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


class SectionTypeTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Math 101")
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.section = Section.objects.create(course=self.course, name="Section A")
        self.section2 = Section.objects.create(course=self.course, name="Section B", section_type=SectionType.LAB)
        self.section3 = Section.objects.create(course=self.course, name="Section C", section_type=SectionType.DISCUSSION)

    def test_default(self):
        self.assertEqual(self.section.section_type, SectionType.LECTURE)
    def test_assigned(self):
        self.assertEqual(self.section2.section_type, SectionType.LAB)
        self.assertEqual(self.section3.section_type, SectionType.DISCUSSION)

class SectionSubsectionTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Test Course")
        self.instructor = User.objects.create_user(username="instructor", password="testpass")
        self.ta = User.objects.create_user(username="ta", password="testpass")
        self.main_section = Section.objects.create(
            name="Lecture 1",
            section_type=SectionType.LECTURE,
            course=self.course,
            instructor=self.instructor,
            schedule={"day": "Monday"}
        )

    def test_is_main_section(self):
        self.assertTrue(self.main_section.is_main_section())
        # Create a subsection and check it's not a main section
        sub = Section.objects.create(
            name="Lab 1",
            section_type=SectionType.LAB,
            course=self.course,
            instructor=self.ta,
            schedule={"day": "Tuesday"},
            main_section=self.main_section
        )
        self.assertFalse(sub.is_main_section())

    def test_is_sub_section(self):
        sub = Section.objects.create(
            name="Lab 1",
            section_type=SectionType.LAB,
            course=self.course,
            instructor=self.ta,
            schedule={"day": "Tuesday"},
            main_section=self.main_section
        )
        self.assertTrue(sub.is_sub_section())
        self.assertFalse(self.main_section.is_sub_section())

    def test_get_subsections_returns_empty_initially(self):
        self.assertEqual(self.main_section.get_subsections().count(), 0)

    def test_get_subsections_returns_created_subsections(self):
        sub1 = self.main_section.create_subsection(
            name="Lab 1",
            sectype=SectionType.LAB,
            instructor=self.ta,
            schedule={"day": "Tuesday"}
        )
        sub2 = self.main_section.create_subsection(
            name="Discussion 1",
            sectype=SectionType.DISCUSSION,
            instructor=self.ta,
            schedule={"day": "Wednesday"}
        )
        subs = self.main_section.get_subsections()
        self.assertIn(sub1, subs)
        self.assertIn(sub2, subs)
        self.assertEqual(subs.count(), 2)

    def test_create_subsection_fails_on_lecture_type(self):
        sub = self.main_section.create_subsection(
            name="Lecture Subsection",
            sectype=SectionType.LECTURE,
            instructor=self.ta,
            schedule={"day": "Thursday"}
        )
        self.assertIsNone(sub)
        self.assertEqual(self.main_section.get_subsections().count(), 0)

    def test_create_subsection_fails_if_not_main_section(self):
        sub = self.main_section.create_subsection(
            name="Lab 1",
            sectype=SectionType.LAB,
            instructor=self.ta,
            schedule={"day": "Tuesday"}
        )
        # Now try to create a subsection under a subsection (should return None)
        subsub = sub.create_subsection(
            name="SubLab",
            sectype=SectionType.LAB,
            instructor=self.ta,
            schedule={"day": "Friday"}
        )
        self.assertIsNone(subsub)
