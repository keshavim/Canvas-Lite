from django.apps import apps
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from webapp.forms import *
from webapp.models import *

def in_groups(group_names):
    def check(user):
        return user.groups.filter(name__in=group_names).exists()
    return user_passes_test(check)

EXCLUDED_MODELS = {"section", "usernotification", "notification"}
@in_groups(["Admin"])
def admin_home(request):
    """shows the admin home page"""
    # Get all models from app that are not in the excluded list
    app_config = apps.get_app_config('webapp')
    model_list = [
        {
            'name': model._meta.verbose_name_plural.title(),
            'admin_url': f'/sudo/{model._meta.model_name}/'
        }
        for model in filter(
            lambda m: m._meta.model_name not in EXCLUDED_MODELS,
            app_config.get_models()
        )
    ]
    return render(request, "admin_pages/dashboard.html", {'models': model_list})


@in_groups(["Admin"])
def courses_list(request):
    courses = Course.objects.prefetch_related('sections').all()
    return render(request, 'admin_pages/list_course.html', {'courses': courses})

@in_groups(["Admin"])
def sections_list(request, model_name, id):
    model = None
    if model_name == "user":
        model = get_object_or_404(User, id=id)
    elif model_name == "course":
        model = get_object_or_404(Course, id=id)
    else:
        Http404("invalid model name")


    sections = model.get_sections()
    return render(request, 'admin_pages/list_sections.html', {
        'model': model,
        'sections': sections,
        "model_name": model_name,
    })

@in_groups(["Admin"])
def user_list(request):
    users = User.objects.prefetch_related(
        'sections_taught'
    )
    return render(request, 'admin_pages/list_user.html', {
        'users': users,
    })


"""
claim views are used by the users view to easily add and remove sections from the user
"""
@in_groups(["Admin"])
def claim_section_list(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    available_sections = Section.objects.filter(instructor__isnull=True)

    filtered_sections = [section for section in available_sections if target_user.is_eligible(section)]

    return render(request, 'admin_pages/claim_section_list.html', {
        'sections': filtered_sections,
        'target_user': target_user,
        'user_id': user_id,
    })


@in_groups(["Admin"])
def claim_section(request,user_id, section_id):
    section = get_object_or_404(Section, id=section_id)
    model = User.objects.get(id=user_id)
    if not section.instructor:  # Prevent claiming already assigned sections
        section.instructor = model
        section.save()
    return redirect('claim_section_list', user_id)
def unclaim_section(request,user_id, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.instructor = None
    section.save()
    return redirect("sections_list", 'user', user_id)


@in_groups(["Admin"])
def manage_section(request, course_id, section_id=None):
    """
    Handles both creation and editing of sections.
    If section_id is provided, edits the section.
    Otherwise, creates a new section for the given course.
    """
    course = get_object_or_404(Course, id=course_id)
    section = get_object_or_404(Section, id=section_id) if section_id else None

    if request.method == 'POST':
        form = SectionForm(
            request.POST,
            instance=section,
            course=course
        )
        if form.is_valid():
            try:
                section_obj = form.save()
                if section:
                    msg = f"Section '{section_obj.name}' updated successfully."
                else:
                    msg = f"Successfully created {section_obj.get_section_type_display()}"
                    if section_obj.main_section:
                        msg += f" under {section_obj.main_section.name}"
                messages.success(request, msg)
                return redirect('sections_list', 'course', course_id)
            except Exception as e:
                messages.error(request, f"Error saving section: {str(e)}")
        else:
            messages.error(request, "Invalid form submission. Please check the errors below.")
    else:
        form = SectionForm(instance=section, course=course)

    context = {
        'form': form,
        'course': course,
        'course_id': course_id,
        'object': section,
        "model_name": "section",
        'type_choices': SectionType.choices,
        'help_texts': {
            'main_section': "Only required for labs/discussions",
            'section_type': "Lectures are main sections, others are subsections"
        }
    }

    # Use the same template for both create and edit
    return render(request, 'admin_pages/manage_sections.html', context)

@in_groups(["Admin"])
def manage_model(request, model_name, model_id=None):
    # Model and form mapping
    model_classes = {
        'course': Course,
        'user': User,
    }
    form_classes = {
        'course': CourseForm,
        'user': UserForm,
    }
    success_urls = {
        'course': 'courses_list',
        'user': 'user_list',
    }

    model_class = model_classes.get(model_name)
    form_class = form_classes.get(model_name)
    if not model_class or not form_class:
        raise Http404("Model not found")

    instance = get_object_or_404(model_class, id=model_id) if model_id else None

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_urls[model_name])
    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
        'object': instance,
        'model_name': model_name,
        model_name: instance if instance else None,
    }

    return render(request, 'admin_pages/manage_models.html', context)


class UniversalDeleteView(DeleteView):
    template_name = 'admin_pages/confirm_delete.html'

    def get_model(self):
        """Get model by name from URL parameter"""
        try:
            return apps.get_model('webapp', self.kwargs['model_name'])
        except LookupError:
            raise Http404("Model not found")

    def get_queryset(self):
        """Return queryset for the detected model"""
        return self.get_model().objects.all()

    def get_success_url(self):
        """Determine success URL based on model"""
        if self.get_model() == User:
            return reverse_lazy('user_list')
        return reverse_lazy('courses_list')





@in_groups(['Admin'])
def messages_list(request):
    users = User.objects.all().order_by('username')
    search = request.GET.get('search', '')
    if search:
        users = users.filter(username__icontains=search)
    selected_user_id = request.GET.get('user')
    sent_notifications = []

    if selected_user_id:
        selected_user = User.objects.get(id=selected_user_id)
        # Only show messages SENT by this user
        sent_notifications = Notification.objects.filter(sender=selected_user).order_by('-created_at')
    else:
        selected_user = None

    # Pagination
    user_paginator = Paginator(users, 20)
    user_page_number = request.GET.get('user_page')
    user_page = user_paginator.get_page(user_page_number)

    notification_paginator = Paginator(sent_notifications, 10)
    notification_page_number = request.GET.get('notification_page')
    notification_page = notification_paginator.get_page(notification_page_number)

    return render(request, 'admin_pages/message_list.html', {
        'user_page': user_page,
        'selected_user': selected_user,
        'notification_page': notification_page,
    })
