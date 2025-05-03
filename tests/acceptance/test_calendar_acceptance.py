from django.test import TestCase, Client
from webapp.models import User

class CalendarPageAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="calendaruser", password="testpass123")

    def test_calendar_requires_login(self):
        response = self.client.get("/calendar/")
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_calendar_loads_for_logged_in_user(self):
        self.client.login(username="calendaruser", password="testpass123")
        response = self.client.get("/calendar/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "standard_pages/calendar.html")
        self.assertContains(response, "Hello, calendaruser")
        self.assertContains(response, "This is your calendar.")
