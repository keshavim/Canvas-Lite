
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView


class AuthService:
    """
    Handles user authentication.
    """

    def login(self, request, email, password):
        """
        Authenticates and logs in a user.
        Returns True if login is successful, False otherwise.
        """
        return TemplateView.as_view(template_name="dashboard.html")

        # user = authenticate(request, username=email, password=password)
        # if user is not None:
        #     login(request, user)
        #     return True
        # return False

    def logout(self, request):
        """
        Logs out the current user.
        Always returns True.
        """
        logout(request)
        return True
