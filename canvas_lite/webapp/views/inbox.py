from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from webapp.models import User, Notification


@login_required
def inbox(request):
    # Only show messages where the current user is a recipient
    notifications = request.user.get_notifications().select_related('notification').order_by('-notification__created_at')

    # Pagination
    notification_paginator = Paginator(notifications, 10)
    notification_page_number = request.GET.get('page')
    notification_page = notification_paginator.get_page(notification_page_number)

    # For the send form
    users = User.objects.exclude(id=request.user.id).order_by('username')

    return render(request, 'standard_pages/inbox.html', {
        'notification_page': notification_page,
        'users': users,
    })

@login_required
def send_notification(request):
    if request.method == 'POST':
        recipient_ids = request.POST.getlist('recipients')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        if 'all_users' in request.POST:
            recipients = User.objects.exclude(id=request.user.id)
        else:
            recipients = User.objects.filter(id__in=recipient_ids)

        Notification.create_and_send(
            recipients=recipients,
            subject=subject,
            message=message,
            sender=request.user
        )
        # For AJAX/modal: return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('inbox')
    return JsonResponse({'status': 'error'}, status=400)
