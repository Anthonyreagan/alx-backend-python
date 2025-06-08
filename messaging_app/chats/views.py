# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ConversationCreateSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # Only show conversations where current user is a participant
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically add current user to participants
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(pk=user_id)
            conversation.participants.add(user)
            return Response(
                {"status": "participant added"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show messages in conversations where user participates
        return Message.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        # Automatically set sender to current user
        conversation_id = self.request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(
                pk=conversation_id,
                participants=self.request.user
            )
            serializer.save(sender=self.request.user, conversation=conversation)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found or access denied"},
                status=status.HTTP_404_NOT_FOUND
            )