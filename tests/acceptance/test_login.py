from django.test import TestCase, Client
from webapp.models import User

class LoginTest(TestCase):

    # acceptance tests for login
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = "user", password = "password")
        self.user.save()

    # test logging in with correct username and password
    def test_login(self):
        #self.client.login(username = "user", password = "password")
        request = self.client.post("/", {"username":"user", "password":"password"}, follow=True)
        self.assertEqual(request.context['username'], "user", "name not passed correctly")
        self.assertEqual(self.client.session.get('username'), "user", "name not passed correctly")
        self.assertEqual(request.status_code, 200)

    # test incorrect password
    def test_incorrectPassword(self):
        request = self.client.post("/",{"username":"user","password":"incorrect"},follow=True)
        self.assertEqual(request.context["message"], "bad password")
        self.assertEqual(request.status_code, 200, "status code not passed from login to list")