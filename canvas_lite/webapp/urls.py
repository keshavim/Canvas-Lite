from django.urls import path

from webapp import views

urlpatterns = [
    path("", views.user_home, name="home"),
    path("sudo/", views.admin_home, name="admin_home"),
    path('sudo/<str:app_label>/<str:model_name>/',
         views.generic_list_view,
         name='admin_model_list'),
    path('admin/<str:app_label>/<str:model_name>/<int:object_id>/edit/',
         views.generic_edit_view,
         name='admin_model_edit'),
    path('admin/<str:app_label>/<str:model_name>/create/',
         views.generic_create_view,
         name='admin_model_create'),

    path("login/", views.user_login, name="user_login"),
]