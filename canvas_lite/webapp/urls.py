from django.urls import path

from webapp import views

urlpatterns = [
    path("", views.user_home, name="home"),
    path("login/", views.user_login, name="user_login"),


#admin urls
    path("sudo/", views.admin_home, name="admin_home"),

#admin stuff do not touch
    path('sudo/course/', views.courses_list, name='courses_list'),
    path('sudo/course/add/', views.add_course, name='add_course'),
    path('sudo/course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('sudo/course/<int:pk>/delete/', views.delete_course.as_view(), name='delete_course'),

    path('sudo/course/<int:course_id>/sections/add/', views.add_section, name='add_section'),
    path('sudo/section/<int:section_id>/edit/', views.edit_section, name='edit_section'),
    path('sudo/section/<int:pk>/delete/', views.delete_section.as_view(), name='delete_section'),

    path('sudo/user/', views.user_list, name='user_list'),
    path('sudo/user/add/', views.add_user, name='add_user'),
    path('sudo/user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('sudo/user/<int:pk>/delete/', views.delete_user.as_view(), name='delete_user'),

    path('sudo/notification/', views.user_notification_list, name='user_notification_list'),
    path('sudo/notification/send/', views.send_notification, name='send_notification'),
#now you can touch

]
