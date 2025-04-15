from django.db import models
from django.contrib.auth.models import AbstractUser

class UserAccount(AbstractUser):
    def __str__(self):
        return self.username

# Profile models (one-to-one linked to UserAccount)

class AdministratorProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    office_number = models.CharField(max_length=100)  # replace placeholder

class InstructorProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)  # replace placeholder

class TeachingAssistantProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    assigned_lab = models.CharField(max_length=100)  # replace placeholder
