from django.test import TestCase, Client
from webapp.models import User

class InboxAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="inboxuser", password="testpass123")

    def test_inbox_requires_login(self):
        response = self.client.get("/inbox/")
        self.assertEqual(response.status_code, 302)

    def test_inbox_loads_for_logged_in_user(self):
        self.client.login(username="inboxuser", password="testpass123")
        response = self.client.get("/inbox/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "standard_pages/inbox.html")
        self.assertContains(response, "Hello, inboxuser")
        self.assertContains(response, "This is your inbox.")
