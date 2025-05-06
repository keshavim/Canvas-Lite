from django.test import TestCase, Client
from webapp.models import User, Course, Section

class CourseIntegrationTestCase(TestCase):
    user_create_url = '/admin/webapp/user/add/'
    course_add_url = '/admin/webapp/course/add/'
    section_create_url = '/webapp/sections/create/'
    assign_instructor_url = '/webapp/sections/1/assign_instructor/'
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.client.login(username='admin', password='adminpass123')

    def test_course_integration(self):
        new_user_data = {
            'username': 'newfaculty',
            'email': 'faculty@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(self.user_create_url, new_user_data, follow=True)  # Replace with actual URL
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newfaculty').exists())
        response = self.client.post(self.course_add_url, {
            'name': 'COMPSCI 361',
            'description': 'Software engineering course'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.course = Course.objects.get(name='COMPSCI 361')
        self.assertTrue(Course.objects.filter(name='COMPSCI 361').exists())
        response = self.client.post(self.section_create_url, {
            'course_id': self.course.id,
            'name': 'Section A',
            'schedule': '{}',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Section.objects.filter(name='Section A', course=self.course).exists())
        section = Section.objects.create(course=self.course, name='Section B')
        response = self.client.post(f'/webapp/sections/{section.id}/assign_instructor/', {
            'instructor_id': self.instructor.id,
        }, follow=True)
        section.refresh_from_db()
        self.assertEqual(section.instructor, self.instructor)