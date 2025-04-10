from django.db import models

#after making a model run this command to make a migrations file
#python manage.py makemigrations "Name of file"

#run this to update the database
#python manage.py migrate


class User(models.Model):
    pass


class courses(models.Model):
    pass

class assinments(models.Model):
    pass

#split up the sections how every you want
#just make sure it is easy to work with so we don't have to spend
#too much time refactoring
class sections(models.Model):
    pass

class Login(models.Model):
    pass