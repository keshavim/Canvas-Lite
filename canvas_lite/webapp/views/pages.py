from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

from webapp.forms import UserForm, UpdateProfileForm
from webapp.models import *
from webapp.models.users import UserType


# views for non-admin users

def user_calendar(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/calendar.html")
    else:
        return redirect("/login")


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/user_profile.html")
    else:
        return redirect("/login")

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect("/profile")
            else:
                 messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'standard_pages/change_password.html', {'form': form})
    else:
        return redirect("/login")

def update_user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("/profile") # Redirect to a success page
        else:
            form = UpdateProfileForm(instance=request.user)
        return render(request, 'standard_pages/update_user_description.html', {'form': form})
    else:
        return redirect("/login")


def user_sections(request):
    user = request.user
    sections = user.get_sections()
    is_instructor = user.group_name == UserType.INSTRUCTOR

    # Print user info to terminal
    print(f"\n=== USER SECTIONS VIEW ===")
    print(f"User: {user.username} (ID: {user.id})")
    print(f"Group: {user.group_name}")
    print(f"Total sections: {sections.count()}")

    main_sections_with_subsections = []
    if is_instructor:
        main_sections = user.get_main_sections()
        print(f"\nMain sections found: {main_sections.count()}")

        for main_section in main_sections:
            subsections = main_section.get_subsections()
            print(f"\nMain Section: {main_section} (ID: {main_section.id})")
            print(f"Subsections: {subsections.count()}")
            for sub in subsections:
                print(f"  - Subsection: {sub} (ID: {sub.id})")

            main_sections_with_subsections.append({
                'main_section': main_section,
                'subsections': subsections,
            })

    # Print regular sections
    print("\nAll sections user is part of:")
    for section in sections:
        print(f"  - Section: {section} (ID: {section.id})")

    context = {
        'sections': sections,
        'is_instructor': is_instructor,
        'main_sections_with_subsections': main_sections_with_subsections,
    }
    return render(request, 'standard_pages/list_courses.html', context)
