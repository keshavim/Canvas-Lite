from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Creates Admins, Instructors, and TAs groups with specific permissions'

    def handle(self, *args, **kwargs):
        # Create or get groups
        admins_group, _ = Group.objects.get_or_create(name='Admin')
        instructors_group, _ = Group.objects.get_or_create(name='Instructor')
        tas_group, _ = Group.objects.get_or_create(name='TA')

        # Get all permissions
        all_permissions = Permission.objects.all()
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        change_permissions = Permission.objects.filter(codename__startswith='change_')

        # Assign all permissions to Admins
        admins_group.permissions.clear()
        admins_group.permissions.add(*all_permissions)
        print("Admin Group created")

        # Assign view and change permissions to Instructors
        instructors_group.permissions.clear()
        instructors_group.permissions.add(*view_permissions, *change_permissions)
        print("Instructor Group created")

        # Assign only view permissions to TAs
        tas_group.permissions.clear()
        tas_group.permissions.add(*view_permissions)
        print("TA Group created")