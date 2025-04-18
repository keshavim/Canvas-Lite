from django.test import TestCase
from django.contrib.auth import get_user_model
from webapp.models import Course, Section, User


class CourseModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Biology 101")
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

    def test_str_representation(self):
        self.assertEqual(str(self.course), "Biology 101")

    def test_get_sections_empty(self):
        self.assertEqual(self.course.get_sections().count(), 0)

    def test_add_section_minimal(self):
        section = self.course.add_section(name="Section A")
        self.assertEqual(section.course, self.course)
        self.assertEqual(section.name, "Section A")
        self.assertIsNone(section.instructor)
        self.assertEqual(section.schedule, {})
        self.assertEqual(self.course.get_sections().count(), 1)

    def test_add_section_with_instructor_and_schedule(self):
        schedule = {"day": "Tuesday", "time": "11:00"}
        section = self.course.add_section(
            name="Section B",
            instructor=self.user1,
            schedule=schedule
        )
        self.assertEqual(section.instructor, self.user1)
        self.assertEqual(section.schedule, schedule)

    def test_add_section_with_assistants(self):
        assistants = [self.user1, self.user2]
        section = self.course.add_section(
            name="Section C",
            assistants=assistants
        )
        self.assertEqual(set(section.assistants.all()), set(assistants))

    def test_get_section_with_id(self):
        section = self.course.add_section(name="Section D")
        fetched = self.course.get_section_with_id(section.id)
        self.assertEqual(fetched, section)

    def test_get_section_with_name(self):
        section = self.course.add_section(name="Section D")
        fetched = self.course.get_section_with_name("Section D")
        self.assertEqual(fetched, section)

    def test_get_section_with_id_not_found(self):
        with self.assertRaises(Section.DoesNotExist):
            self.course.get_section_with_id(9999)

    def test_remove_section_success(self):
        section = self.course.add_section(name="Section E")
        result = self.course.remove_section(section.id)
        self.assertTrue(result)
        self.assertEqual(self.course.get_sections().count(), 0)

    def test_remove_section_failure(self):
        result = self.course.remove_section(9999)
        self.assertFalse(result)
