# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users who are participants of the conversation
    to view or modify it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):  # for Conversation objects
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):  # for Message objects
            is_participant = request.user in obj.conversation.participants.all()

            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return is_participant and request.user == obj.sender

            return is_participant

        return False
