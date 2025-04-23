from django.urls import path

from webapp.views import user_login, user_register, user_home, user_admin_home



urlpatterns = [
    path("", user_home, name="dashboard"),
    path("sudo/", user_admin_home, name="dashboard"),

    path("login/", user_login, name="login"),
    path("register/", user_register, name="signup"),

]