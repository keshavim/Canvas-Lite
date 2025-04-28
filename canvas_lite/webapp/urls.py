from django.urls import path

from webapp import views

urlpatterns = [
    path("", views.user_home, name="home"),
    path("login/", views.user_login, name="user_login"),


#admin urls
    path("sudo/", views.admin_home, name="admin_home"),

#admin stuff do not touch
    path('sudo/course/', views.courses_list, name='courses_list'),

    path('sudo/user/', views.user_list, name='user_list'),

    path('add/<str:model_name>/', views.add_model, name='add_model_generic'),
    path('add/<str:model_name>/<int:course_id>/', views.add_model, name='add_model_section'),

    path('sudo/<str:model_name>/<int:model_id>/edit', views.edit_model, name='edit_model'),

    path('sudo/<str:model_name>/delete/<int:pk>/', views.UniversalDeleteView.as_view(), name='delete_model'),



    path('sudo/notification/', views.user_notification_list, name='user_notification_list'),
    path('sudo/notification/send/', views.send_notification, name='send_notification'),
#now you can touch

]
