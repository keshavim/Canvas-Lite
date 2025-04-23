import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
"""
current users

mike
Tf-&_'neA6~!^;9P2,cu$)

testuser2
UdQ,C?x['c/~7:.s95pT;a


keshab
keshab123

testuser
testuser123

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
