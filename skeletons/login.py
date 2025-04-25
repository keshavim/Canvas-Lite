#
# from django.contrib.auth import authenticate, login, logout
# from django.views.generic import TemplateView
#
#
# class AuthService:
#     """
#     Handles webapp authentication.
#     """
#
#     def login(self, request, email, password):
#         """
#         Authenticates and logs in a webapp.
#         Returns True if login is successful, False otherwise.
#         """
#         # webapp = authenticate(request, username=email, password=password)
#         # if webapp is not None:
#         #     login(request, webapp)
#         #     return True
#         # return False
#         pass
#
#     def logout(self, request):
#         """
#         Logs out the current webapp.
#         Always returns True.
#         """
#         pass

"""
    Function that allows a user to login.
    Parameters:
    username (string): Username of user logging in
    password (string): Password of user logging in
    current_users (list): List of users logged in, note that users are objects in this case
    users (list): List of all users, note that users are objects in this case
    Preconditions: username and password are set, user is not logged in.
    Postconditions: user is logged in if password is correct (return True),
    user is added to current_users list.
    Not logged in otherwise (return False).
"""


def login(username, password, current_users, users):
    for user in users:
        if user.username == username and user not in current_users and user.password == password:
            current_users.append(user)
            return True
    return False


"""
    Function that allows a user to logout.
    Parameters: 
    username (string): Username of user logging out
    current_users (list): List of users logged in
    Preconditions: user is logged in.
    Postconditions: user is logged out if currently logged in (return True),
    user is removed from current_users list. 
    Nothing happens otherwise (return False).
"""


def logout(username, current_users):
    for user in current_users:
        if user.username == username:
            current_users.remove(user)
            return True
    return False
