import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
"""
current users
mike
keshavim123

superkesha
kesha123

jacky
123

bob12
1234
"""

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        if users.exists():
            self.stdout.write('List of all users:')
            for user in users:
                self.stdout.write(f'Username: {user.username}, First Name: {user.first_name}, Last Name: {user.last_name}')
        else:
            self.stdout.write('No users found in the database.')
