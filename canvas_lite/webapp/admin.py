from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import *
from .forms import UserRegistrationForm

class CustomUserAdmin(UserAdmin):
    register_form = UserRegistrationForm
    model = User
    list_display = ["username", "email", "is_staff", "is_active"]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Notification)

