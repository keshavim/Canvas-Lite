from django.db import models

#after making a model run this command to make a migrations file
#python manage.py makemigrations "Name of file"

#run this to update the database
#python manage.py migrate


class User(models.Model):
    def login(self):
        pass
    def logout(self):
        pass
    def createAccount(self):
        pass
    def editAccountInfo(self):
        pass
