
from django.contrib.auth import authenticate, login, logout

class AuthService:
    """
    Handles user authentication.
    """

    def login(self, request, email, password):
        """
        Authenticates and logs in a user.
        Returns True if login is successful, False otherwise.
        """
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return True
        return False

    def logout(self, request):
        """
        Logs out the current user.
        Always returns True.
        """
        logout(request)
        return True
