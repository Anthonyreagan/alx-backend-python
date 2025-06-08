# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to ensure the user is a participant in the conversation.
    """

    def has_permission(self, request, view):
        # Only allow access if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Conversation object
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Message object
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False
