from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#
# from .models import UserAccount, AdministratorProfile, InstructorProfile, TeachingAssistantProfile

from .models.users import User
from .forms import UserRegistrationForm

class CustomUserAdmin(UserAdmin):
    register_form = UserRegistrationForm
    model = User
    list_display = ["username", "email", "is_staff", "is_active"]

admin.site.register(User, CustomUserAdmin)

