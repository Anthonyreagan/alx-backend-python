from django.shortcuts import render
from django.db.models import Q  # Add this import
from rest_framework import viewsets, status, mixins, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)


class ConversationViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin):
    """
    API endpoint for conversations that allows:
    - Listing conversations
    - Creating new conversations
    - Retrieving conversation details
    """
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['updated_at']
    search_fields = ['participants__username']

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # Only return conversations where current user is a participant
        return self.queryset.filter(participants=self.request.user).order_by('-updated_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create conversation and add current user as participant
        conversation = serializer.save()
        conversation.participants.add(request.user)

        # Return full conversation details
        output_serializer = ConversationSerializer(conversation, context={'request': request})
        headers = self.get_success_headers(output_serializer.data)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for a specific conversation"""
        conversation = self.get_object()
        # Verify user is a participant in this conversation
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        messages = Message.objects.filter(conversation=conversation).order_by('sent_at')
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    """
    API endpoint for messages that allows:
    - Listing messages
    - Creating new messages
    - Retrieving message details
    """
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['sent_at']
    search_fields = ['content']

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        # Only show messages where current user is a participant in the conversation
        user = self.request.user
        queryset = self.queryset.filter(
            Q(conversation__participants=user) &
            (Q(sender=user) | Q(conversation__participants=user))
        ).order_by('-sent_at')

        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset
        Message.objects.filter(Q(sender=user) | Q(receiver=user))



    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to ensure message belongs to user"""
        instance = self.get_object()
        if not instance.conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify user is a participant in the conversation
        conversation = serializer.validated_data['conversation']
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Set the current user as sender
        message = serializer.save(sender=request.user)

        # Update conversation's updated_at timestamp
        conversation.save()  # This will auto-update the timestamp

        # Return full message details
        output_serializer = MessageSerializer(message, context={'request': request})
        headers = self.get_success_headers(output_serializer.data)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )