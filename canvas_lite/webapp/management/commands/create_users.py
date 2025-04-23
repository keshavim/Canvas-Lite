from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from webapp.models import User


users_info = [
    {
        'username': 'admin_user',
        'password': 'adminpass123',
        'email': 'admin@example.com',
        'group': 'Admin'
    },
    {
        'username': 'instructor_user',
        'password': 'instructorpass123',
        'email': 'instructor@example.com',
        'group': 'Instructor'
    },
    {
        'username': 'ta_user',
        'password': 'tapass123',
        'email': 'ta@example.com',
        'group': 'TA'
    },
]


class Command(BaseCommand):
    help = 'Creates Admins, Instructors, and TAs groups with specific permissions'

    def handle(self, *args, **kwargs):
        for info in users_info:
            # Create user if not exists
            user, created = User.objects.get_or_create(username=info['username'], defaults={
                'email': info['email']
            })
            if created:
                user.set_password(info['password'])
                user.save()
                print(f"Created user: {info['username']}")
            else:
                print(f"User {info['username']} already exists.")

            # Get group and add user to group
            try:
                group = Group.objects.get(name=info['group'])
                user.groups.add(group)
                print(f"Added {info['username']} to {info['group']}")
            except Group.DoesNotExist:
                print(f"Group {info['group']} does not exist. Please create it first.")

        print("Users created.")
