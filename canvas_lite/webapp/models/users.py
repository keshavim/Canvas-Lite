from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models




class User(AbstractUser):



    def __str__(self):
        return self.username

    class Meta:
        permissions = (
            ("can_assign_l1", "Can assign to courses/sections: instructor"),
            ("can_assign_l2", "Can assign to courses/sections: admin"),
        )
