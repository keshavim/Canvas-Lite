from django.db import models

from the_app.models.models import User


#after making a model run this command to make a migrations file
#python manage.py makemigrations "Name of file"

#run this to update the database
#python manage.py migrate

class TeachingAssistant(models.Model, User):
    pass
