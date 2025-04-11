from django.db import models

#after making a model run this command to make a migrations file
#python manage.py makemigrations "Name of file"

#run this to update the database
#python manage.py migrate
from the_app.models.models import User


class Instructor(models.Model, User):
    def assinTa(self):
        pass
    def readUserInfo(self):
        pass
    def viewAssinments(self):
        pass