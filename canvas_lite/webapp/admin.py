from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import *



class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "is_staff", "is_active"]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Notification)

