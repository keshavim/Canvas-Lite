from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from webapp.forms import SendMessageForm
from webapp.models import User, Notification, UserNotification


def user_in_group(request, group_name):
    user = request.user
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

@login_required
def inbox(request):
    box = request.GET.get('box', 'received')  # Default to 'received'

    #inbox part
    if box == 'sent':
        # Messages where the current user is the sender
        notifications = request.user.get_sent_notifications().order_by('-created_at')
        # Note: No need for .select_related('notification') here, since these are Notification objects
        user_notifications = [
            {'notification': n, 'read': True, 'read_at': n.created_at}
            for n in notifications
        ]
    else:
        # Messages where the current user is a recipient
        notifications = request.user.get_notifications().order_by(
            '-notification__created_at')
        user_notifications = notifications

    notification_paginator = Paginator(user_notifications, 10)
    notification_page_number = request.GET.get('page')
    notification_page = notification_paginator.get_page(notification_page_number)

    users = User.objects.exclude(id=request.user.id).order_by('username')
    group_name = request.user.group_name


    #send part
    if request.method == 'POST':
        form = SendMessageForm(request.POST, user=request.user)
        if form.is_valid():
            all_users = form.cleaned_data['all_users']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            if all_users:
                recipients = User.objects.exclude(id=request.user.id)
            else:
                recipients = form.cleaned_data['recipients']

            request.user.send_notifications(recipients=recipients, subject=subject, message=message)

            messages.success(request, "Message sent successfully!")
            if request.user.group_name == "Admin":
                return redirect('admin_inbox')
            else:
                return redirect('user_inbox')
    else:
        # Initial form for GET requests
        form = SendMessageForm(user=request.user)

    return render(request, 'standard_pages/inbox.html', {
        'form': form,
        'notification_page': notification_page,
        'users': users,
        'group_name': group_name,
        'box': box,
    })

def toggle_notification_read(request, nid):
    notification = UserNotification.objects.get(id=nid)
    if notification.read:
        notification.mark_as_unread()
    else:
        notification.mark_as_read()
    # Redirect back to the page you came from or a default page
    return redirect(request.META.get('HTTP_REFERER', 'notifications:list'))
