from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def user_admin_home(request):
    """shows the admin home page"""
    # Get all models from app
    app_config = apps.get_app_config('webapp')
    model_list = []
    for model in app_config.get_models():
        model_list.append({
            'name': model._meta.verbose_name_plural.title(),
            'admin_url': f'/sudo/{model._meta.model_name}/',
        })
    return render(request, "admin_pages/dashboard.html", {'models': model_list})