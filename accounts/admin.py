from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#
# from .models import UserAccount, AdministratorProfile, InstructorProfile, TeachingAssistantProfile
#
# class AdministratorProfileInline(admin.StackedInline):
#     model = AdministratorProfile
#
# class InstructorProfileInline(admin.StackedInline):
#     model = InstructorProfile
#
# class TeachingAssistantProfileInline(admin.StackedInline):
#     model = TeachingAssistantProfile
#
#
# class SiteAdmin(UserAdmin):
#     add_form = CustomCreationForm
#     form = CustomChangeForm
#     model = UserAccount
#     list_display = [
#         "email",
#         "username",
#         "is_staff",
#         "is_active",
#     ]

    #don't worry about this, just setting some stuff up for the future
    # Add inlines for profiles based on the user type
    # def get_inline_instances(self, request, obj=None):
    #     if obj:
    #         if obj.is_superuser:  # Administrator logic (or check a custom role field)
    #             return [AdministratorProfileInline(self.model, self.admin_site)]
    #         elif obj.groups.filter(name="Instructor").exists():  # Instructor logic
    #             return [InstructorProfileInline(self.model, self.admin_site)]
    #         elif obj.groups.filter(name="TA").exists():  # TA logic
    #             return [TeachingAssistantProfileInline(self.model, self.admin_site)]
    #     return []



# Register your models here.
#admin.site.register(UserAccount, SiteAdmin)
# admin.site.register(AdministratorProfile)
# admin.site.register(InstructorProfile)
# admin.site.register(TeachingAssistantProfile)

