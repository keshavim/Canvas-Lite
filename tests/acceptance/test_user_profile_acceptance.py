from django.test import TestCase, Client
from webapp.models import User

class UserProfileAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="profileuser", password="testpass123")

    def test_user_profile_requires_login(self):
        response = self.client.get("/profile/", follow=True)
        self.assertRedirects(response, "/login/", status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_loads_for_logged_in_user(self):
        self.client.login(username="profileuser", password="testpass123")
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "standard_pages/user_profile.html")
        self.assertContains(response, "Hello, profileuser")
        self.assertContains(response, "This is your profile view.")
        self.assertContains(response, "Change Password")
