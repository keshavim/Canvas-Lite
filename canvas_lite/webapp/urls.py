from django.urls import path

from webapp import views

urlpatterns = [
    path("", views.user_home, name="home"),
    path("login/", views.user_login, name="user_login"),


#admin urls
    path("sudo/", views.admin_home, name="admin_home"),
    path('sudo/course/', views.courses_list, name='courses_list'),
    path('sudo/course/add/', views.add_course, name='add_course'),
    path('sudo/course/<int:course_id>/sections/add/', views.add_section, name='add_section'),
    path('sudo/course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('sudo/section/<int:course_id>/<int:section_id>/edit/', views.edit_section, name='edit_section'),

]

# path('sudo/<str:app_label>/<str:model_name>/',
#      views.generic_list_view,
#      name='admin_model_list'),
# path('admin/<str:app_label>/<str:model_name>/<int:object_id>/edit/',
#      views.generic_edit_view,
#      name='admin_model_edit'),
# path('admin/<str:app_label>/<str:model_name>/create/',
#      views.generic_create_view,
#      name='admin_model_create'),