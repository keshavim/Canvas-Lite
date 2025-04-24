from django.apps import apps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory

from webapp.forms import AdminUserEditForm
from webapp.models import User

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
            'admin_url': f'/sudo/{model._meta.app_label}/{model._meta.model_name}/',
        })
        print(model._meta.model_name)
    return render(request, "admin_pages/dashboard.html", {'models': model_list})

@in_groups(["Admin"])
def generic_list_view(request, app_label, model_name):
    model = apps.get_model(app_label, model_name)
    objects = model.objects.all()
    return render(request, 'admin_pages/list_model.html', {
        'objects': objects,
        'model_name': model_name,
        'app_label': app_label,
    })

in_groups(["Admin"])(generic_list_view)
def generic_create_view(request, app_label, model_name):
    model = apps.get_model(app_label, model_name)
    # You can customize fields per model if needed
    fields = '__all__'
    form_class = modelform_factory(model, fields=fields)
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_model_list', app_label=app_label, model_name=model_name)
    else:
        form = form_class()
    return render(request, 'admin_pages/create_model.html', {
        'form': form,
        'model_name': model_name,
        'app_label': app_label,
    })


# Define which fields to show for each model
EDITABLE_FIELDS = {
    'user': ['first_name', 'last_name', 'email', 'group_name', 'is_active'],
    'course': ['name', 'description'],
    'section': ['name', 'schedule', 'section_type', 'course', 'instructor', 'main_section'],
    'notification': ['subject', 'message', 'sender', 'recipients'],
    # etc.
}

@in_groups(["Admin"])
def generic_edit_view(request, app_label, model_name, object_id):
    model = apps.get_model(app_label, model_name)
    instance = get_object_or_404(model, id=object_id)
    fields = EDITABLE_FIELDS.get(model_name.lower(), '__all__')
    form_class = modelform_factory(model, fields=fields)
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('admin_model_list', app_label=app_label, model_name=model_name)
    else:
        form = form_class(instance=instance)
    return render(request, 'admin_pages/edit_model.html', {
        'form': form,
        'object': instance,
        'model_name': model_name,
        'app_label': app_label,
    })

