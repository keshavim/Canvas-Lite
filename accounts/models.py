from django.contrib.auth.models import AbstractUser
from django.db import models



#testing on ta first will adapt to the others after ta works
#
# class UserAccount(AbstractUser):
#     pass
#
#     def __str__(self):
#         return self.username
#
#
# #to do add the groups
#
# class AdministratorProfile(models.Model):
#     user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
#     admin_specific_field = models.CharField(max_length=100)
#
# class InstructorProfile(models.Model):
#     user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
#     instructor_specific_field = models.CharField(max_length=100)
#
# class TeachingAssistantProfile(models.Model):
#     user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
#     ta_specific_field = models.CharField(max_length=100)