# chats/permissions.py

from rest_framework.permissions import BasePermission

class IsParticipantOrSender(BasePermission):
    """
    Custom permission to only allow participants of a conversation to view messages,
    or the sender to manage their own messages.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If it's a Message instance
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all() or obj.sender == user

        # If it's a Conversation instance
        return user in obj.participants.all()
