from django.test import TestCase
from webapp.models import User, Course, Section

class SectionAcceptanceTest(TestCase):
    def setUp(self):
        # Create sample users
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='admin')
        self.instructor = User.objects.create_user(username='instructor', password='instructorpass', role='instructor')
        self.ta = User.objects.create_user(username='tauser', password='tapass', role='ta')

        # Create a course assigned to the instructor
        self.course = Course.objects.create(
            title='Intro to CS',
            semester='Fall 2025',
            instructor=self.instructor
        )

        self.section_create_url = '/webapp/sections/create/'
        self.assign_instructor_url = '/webapp/sections/1/assign_instructor/'
        self.assign_ta_url = '/webapp/sections/1/assign_tas/'
        self.set_schedule_url = '/webapp/sections/1/set_schedule/'

    def test_create_section_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(self.section_create_url, {
            'course_id': self.course.id,
            'name': 'Section A',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Section.objects.filter(name='Section A', course=self.course).exists())

    def test_assign_instructor_to_section(self):
        section = Section.objects.create(course=self.course, name='Section B')
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(f'/webapp/sections/{section.id}/assign_instructor/', {
            'instructor_id': self.instructor.id,
        }, follow=True)
        section.refresh_from_db()
        self.assertEqual(section.instructor, self.instructor)

    def test_assign_ta_to_section(self):
        section = Section.objects.create(course=self.course, name='Section C')
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(f'/webapp/sections/{section.id}/assign_tas/', {
            'assistant_ids': [self.ta.id],
        }, follow=True)
        section.refresh_from_db()
        self.assertEqual(self.ta, self.instructor)

    def test_set_schedule_for_section(self):
        section = Section.objects.create(course=self.course, name='Section D')
        self.client.login(username='admin', password='adminpass')
        schedule = {
            "day": "Tuesday",
            "time": "10AM-12PM",
            "location": "Room 202"
        }
        response = self.client.post(f'/webapp/sections/{section.id}/set_schedule/', {
            'schedule': schedule
        }, follow=True)
        section.refresh_from_db()
        self.assertEqual(section.schedule.get('day'), 'Tuesday')
        self.assertEqual(section.schedule.get('location'), 'Room 202')
