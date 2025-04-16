
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView


class AuthService:
    """
    Handles webapp authentication.
    """

    def login(self, request, email, password):
        """
        Authenticates and logs in a webapp.
        Returns True if login is successful, False otherwise.
        """
        # webapp = authenticate(request, username=email, password=password)
        # if webapp is not None:
        #     login(request, webapp)
        #     return True
        # return False
        pass

    def logout(self, request):
        """
        Logs out the current webapp.
        Always returns True.
        """
        pass
