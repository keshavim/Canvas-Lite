from django.db import models

#after making a model run this command to make a migrations file
#python manage.py makemigrations "Name of file"

#run this to update the database
#python manage.py migrate
from the_app.models.models import User


class Supervisor(models.Model, User):
    def createCourses(self):
        pass
    def deleteCourses(self):
        pass
    def createOtherAccount(self):
        pass
    def deleteOtherAccounts(self):
        pass
    def sendNotificatons(self):
        pass
