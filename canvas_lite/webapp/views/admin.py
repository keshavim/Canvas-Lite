from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from webapp.forms import *
from webapp.models import *

def in_groups(group_names):
    def check(user):
        return user.groups.filter(name__in=group_names).exists()
    return user_passes_test(check)


@in_groups(["Admin"])
def admin_home(request):
    """shows the admin home page"""
    # Get all models from app
    app_config = apps.get_app_config('webapp')
    model_list = []
    for model in app_config.get_models():
        model_list.append({
            'name': model._meta.verbose_name_plural.title(),
            'admin_url': f'/sudo/{model._meta.model_name}/',
        })
        print(model._meta.model_name)
    return render(request, "admin_pages/dashboard.html", {'models': model_list})



def courses_list(request):
    courses = Course.objects.all().prefetch_related('sections')
    return render(request, 'admin_pages/list_course.html', {'courses': courses})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin_pages/edit_course.html', {'form': form, 'course': course})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('courses_list')
    else:
        form = CourseForm()
    return render(request, 'admin_pages/add_course.html', {'form': form})

class delete_course(DeleteView):
    model = Course
    template_name = 'admin_pages/confirm_delete.html'
    success_url = reverse_lazy('courses_list')


def edit_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = SectionForm(instance=section)
    return render(request, 'admin_pages/edit_section.html', {'form': form, 'section': section})

def add_section(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            messages.success(request, 'Section added successfully!')
            return redirect('courses_list')
    else:
        form = SectionForm()

    return render(request, 'admin_pages/add_section.html', {
        'form': form,
        'course': course
    })

class delete_section(DeleteView):
    model = Section
    template_name = 'admin_pages/confirm_delete.html'
    success_url = reverse_lazy('courses_list')



def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_pages/list_user.html', {
        'users': users,
    })

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'admin_pages/edit_user.html', {
        'form': form,
        'user': user,
    })

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'admin_pages/add_user.html', {
        'form': form,
    })
class delete_user(DeleteView):
    model = User
    template_name = 'admin_pages/confirm_delete.html'
    success_url = reverse_lazy('user_list')
