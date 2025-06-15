
#!/usr/bin/env python3
from django.shortcuts import render
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from .models import Message, Notification, Conversation, UnreadMessagesManager



@cache_page(60)  # Cache this view for 60 seconds
def message_list(request):
    messages = Message.objects.select_related('sender', 'conversation') \
                .prefetch_related('replies') \
                .order_by('-timestamp')
    return render(request, 'messaging/messages.html', {'messages': messages})


def threaded_conversation_view(request, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)
    messages = Message.objects.filter(conversation=conversation, parent_message__isnull=True) \
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender').order_by('timestamp'))
        ).order_by('timestamp')

    return render(request, 'messaging/threaded_conversation.html', {
        'conversation': conversation,
        'messages': messages
    })


def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'messaging/notifications.html', {'notifications': notifications})



def unread_messages(request):
    # Use the custom manager's method to get unread messages for the current user
    messages = Message.unread.for_receiver(request.user)
    return render(request, 'messaging/unread_messages.html', {'unread_messages': messages})


def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return render(request, 'messaging/account_deleted.html', {
        'user': user,
        'message': 'Your account has been deleted successfully.'
    })
