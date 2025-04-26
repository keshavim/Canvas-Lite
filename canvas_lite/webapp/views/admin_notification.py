from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from webapp.models import Notification, UserNotification, User

def in_groups(group_names):
    def check(user):
        return user.groups.filter(name__in=group_names).exists()
    return user_passes_test(check)


@in_groups('Admin')
def user_notification_list(request):
    users = User.objects.all().order_by('username')
    selected_user_id = request.GET.get('user')
    notifications = []

    if selected_user_id:
        selected_user = User.objects.get(id=selected_user_id)
        notifications = selected_user.get_notifications().select_related('notification')
    else:
        selected_user = None

    # Pagination
    user_paginator = Paginator(users, 20)  # Show 20 users per page
    user_page_number = request.GET.get('user_page')
    user_page = user_paginator.get_page(user_page_number)

    notification_paginator = Paginator(notifications, 10)  # Show 10 notifications per page
    notification_page_number = request.GET.get('notification_page')
    notification_page = notification_paginator.get_page(notification_page_number)

    return render(request, 'admin_pages/notif/user_list.html', {
        'user_page': user_page,
        'selected_user': selected_user,
        'notification_page': notification_page,
    })

@in_groups('Admin')
@require_http_methods(["POST"])
def send_notification(request):
    recipient_ids = request.POST.getlist('recipients')
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')

    if 'all_users' in request.POST:
        recipients = User.objects.all()
    else:
        recipients = User.objects.filter(id__in=recipient_ids)

    Notification.create_and_send(
        recipients=recipients,
        subject=subject,
        message=message,
        sender=request.user
    )

    return redirect('user_notification_list')
