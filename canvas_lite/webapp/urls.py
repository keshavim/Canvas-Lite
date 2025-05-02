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
    path('sudo/<str:model_name>/<int:id>/section/', views.sections_list, name='sections_list'),

    path('sudo/create/<str:model_name>/', views.create_model, name='create_model'),
    path('sudo/create/section/<int:course_id>/', views.create_section, name='create_model_section'),

    path('sudo/<int:user_id>/claim-sections/', views.claim_section_list, name='claim_section_list'),
    path('sudo/<int:user_id>/claim-section/<int:section_id>/', views.claim_section, name='claim_section'),
    path('sudo/<int:user_id>/unclaim_claim-section/<int:section_id>/', views.unclaim_section, name='unclaim_section'),

    path('sudo/<str:model_name>/<int:model_id>/edit', views.edit_model, name='edit_model'),

    path('sudo/<str:model_name>/delete/<int:pk>/', views.UniversalDeleteView.as_view(), name='delete_model'),



    path('sudo/notification/', views.user_notification_list, name='user_notification_list'),
    path('sudo/notification/send/', views.send_notification, name='send_notification'),
#now you can touch

    # standard_pages for non-admin users
    path('calendar/', views.user_calendar, name='user_calendar'),

    path('courses/', views.user_courses, name='user_courses'),

    path('inbox/', views.user_inbox, name='user_inbox'),


    path('profile/', views.user_profile, name='user_profile'),

    path('change_password/', views.change_password, name='change_password'),

]
