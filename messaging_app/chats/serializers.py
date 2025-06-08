from rest_framework import serializers
from .models import User, Conversation, Message
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    # Adding SerializerMethodField example
    full_name = serializers.SerializerMethodField()
    # Adding CharField example
    status = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="User's status message"
    )

    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'profile_picture',
            'status',
            'last_seen'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_picture': {'required': False}
        }

    # SerializerMethodField implementation
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    # ValidationError example
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value.lower()


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # CharField example with custom validation
    message_body = serializers.CharField(
        max_length=2000,
        error_messages={
            'blank': "Message cannot be empty.",
            'max_length': "Message is too long (max 2000 characters)."
        }
    )

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
            'read'
        ]
        read_only_fields = ['sent_at']

    # ValidationError example
    def validate(self, data):
        if len(data.get('message_body', '').strip()) < 1:
            raise serializers.ValidationError({
                'message_body': "Message cannot be empty."
            })
        return data


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    # SerializerMethodField example
    participant_count = serializers.SerializerMethodField()
    # CharField example for search
    search_term = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Search term for filtering participants"
    )

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_count',
            'created_at',
            'updated_at',
            'messages',
            'search_term'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_participant_count(self, obj):
        return obj.participants.count()

    # ValidationError example
    def validate_participants(self, participants):
        if len(participants) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants."
            )
        return participants


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True
    )
    # CharField example for optional conversation topic
    topic = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'topic']

    def create(self, validated_data):
        try:
            participants = validated_data.pop('participants')
            conversation = Conversation.objects.create(**validated_data)
            conversation.participants.set(participants)
            return conversation
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))