from rest_framework import serializers
from .models import User, Conversation, Message
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'profile_picture', 'status', 'last_online']
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only': True}
        }

    def create(self, validated_data):
        # Hash password before saving
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'read']
        read_only_fields = ['message_id', 'sent_at', 'read']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at',
                  'updated_at', 'messages', 'last_message']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=True
    )

    class Meta:
        model = Conversation
        fields = ['participants']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Conversation must have at least 2 participants")
        return value


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['conversation', 'message_body']
        extra_kwargs = {
            'conversation': {'required': True},
            'message_body': {'required': True}
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'user_id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)