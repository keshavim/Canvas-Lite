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

    path('sudo/<str:model_name>/create/', views.manage_model, name='create_model'),
    path('sudo/<str:model_name>/<int:model_id>/edit/', views.manage_model, name='edit_model'),

# urls.py
    path('sudo/section/create/<int:course_id>/', views.manage_section, name='create_section'),
    path('sudo/section/<int:course_id>/edit/<int:section_id>/', views.manage_section, name='edit_section'),

    path('sudo/<int:user_id>/claim-sections/', views.claim_section_list, name='claim_section_list'),
    path('sudo/<int:user_id>/claim-section/<int:section_id>/', views.claim_section, name='claim_section'),
    path('sudo/<int:user_id>/unclaim_claim-section/<int:section_id>/', views.unclaim_section, name='unclaim_section'),

    path('sudo/<str:model_name>/delete/<int:pk>/', views.UniversalDeleteView.as_view(), name='delete_model'),

    path('sudo/notification/', views.inbox, name='admin_inbox'),
    path('sudo/all_messages/', views.messages_list, name='messages_list'),

    # path('send-notification/', views.send_notification, name='send_notification'),
    path('inbox/', views.inbox, name='user_inbox'),
    path('inbox/<int:nid>/toggle/', views.toggle_notification_read, name='toggle_notification_read'),

    path('courses/', views.user_sections, name='user_courses'),
    path('course/<int:section_id>/', views.section_detail, name='section_detail'),
    path('section/<int:section_id>/assign-instructor/', views.manage_subsection_instructor, name='assign_subsection_instructor'),

    # standard_pages for non-admin users
    path('calendar/', views.user_calendar, name='user_calendar'),


    path('profile/', views.user_profile, name='user_profile'),

    path('inbox/', views.inbox, name='user_inbox'),

    path('change_password/', views.change_password, name='change_password'),

    path("update_description/", views.update_user_profile, name="update_user_profile"),

]
