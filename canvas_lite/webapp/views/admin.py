from django.apps import apps
from django.contrib.auth.decorators import user_passes_test
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

EXCLUDED_MODELS = {"section", "usernotification"}
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



def courses_list(request):
    courses = Course.objects.all().prefetch_related('sections')
    return render(request, 'admin_pages/list_course.html', {'courses': courses})


def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_pages/list_user.html', {
        'users': users,
    })


def add_model(request, model_name, course_id=None):
    # Configuration dictionaries
    model_config = {
        'course': {
            'form_class': CourseForm,
            'success_url': 'courses_list',
            'extra_context': {}
        },
        'section': {
            'form_class': SectionForm,
            'success_url': 'courses_list',
            'extra_context': lambda: {'course': get_object_or_404(Course, id=course_id)},
            'form_kwargs': lambda: {'course': get_object_or_404(Course, id=course_id)}
        },
        'user': {
            'form_class': UserForm,
            'success_url': 'user_list',
            'extra_context': {},
            'post_save': lambda form: form.save()  # Custom save for user if needed
        }
    }

    config = model_config.get(model_name)
    if not config:
        raise Http404("Model not supported")

    # Handle form kwargs
    form_kwargs = {}
    if 'form_kwargs' in config:
        form_kwargs = config['form_kwargs']()

    if request.method == 'POST':
        form = config['form_class'](request.POST, **form_kwargs)
        if form.is_valid():
            if 'post_save' in config:
                config['post_save'](form)
            else:
                form.save()
            return redirect(config['success_url'])
    else:
        form = config['form_class'](**form_kwargs)

    # Build context
    context = {
        'form': form,
        'model_name': model_name,
        'course_id': course_id,
    }

    if 'extra_context' in config:
        extra = config['extra_context']() if callable(config['extra_context']) else config['extra_context']
        context.update(extra)

    template_name = 'admin_pages/add_model.html'

    return render(request, template_name, context)




def edit_model(request, model_name, model_id):
    # Model mapping dictionary
    model_classes = {
        'course': Course,
        'section': Section,
        'user': User
    }

    # Form mapping dictionary
    form_classes = {
        'course': CourseForm,
        'section': SectionForm,
        'user': UserForm
    }

    # URL mapping for redirects
    success_urls = {
        'course': 'courses_list',
        'section': 'courses_list',
        'user': 'user_list'
    }

    model_class = model_classes.get(model_name)
    form_class = form_classes.get(model_name)

    if not model_class or not form_class:
        raise Http404("Model not found")

    instance = get_object_or_404(model_class, id=model_id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_urls[model_name])
    else:
        form = form_class(instance=instance)

    # Template paths should follow the pattern 'admin_pages/edit_{model_name}.html'
    template_name = f'admin_pages/edit_model.html'

    context = {
        'form': form,
        'object': instance,  # Generic object reference
        'model_name': model_name,  # Explicit model name
        model_name: instance  # Maintain backward compatibility
    }

    return render(request, template_name, context)



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

