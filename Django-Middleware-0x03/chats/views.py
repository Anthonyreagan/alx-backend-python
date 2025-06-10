# chats/views.py
from .filters import MessageFilter
from .pagination import MessagePagination
from .permissions import IsParticipantOfConversation
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend


from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['participants']  # or fields you want to filter by
    search_fields = ['title', 'description']  # example, update per your model
    ordering_fields = ['created_at']  # example, update per your model

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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sender', 'conversation']
    search_fields = ['content']  # or whatever text fields you have
    ordering_fields = ['timestamp']
    pagination_class = MessagePagination
    filterset_class = MessageFilter



    def get_queryset(self):
        return Message.objects.filter(
            conversation__conversation_id=self.kwargs['conversation_pk'],
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        try:
            conversation = Conversation.objects.get(
                conversation_id=self.kwargs['conversation_pk'],
                participants=self.request.user
            )
            serializer.save(sender=self.request.user, conversation=conversation)
        except Conversation.DoesNotExist:
            raise ValidationError({"error": "Conversation not found or access denied"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.sender:
            return Response({"detail": "Not allowed to delete this message."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.sender:
            raise PermissionDenied("You are not the sender of this message.")
        return super().update(request, *args, **kwargs)