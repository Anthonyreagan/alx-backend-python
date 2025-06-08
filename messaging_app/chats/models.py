import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser with additional fields"""
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        null=False
    )
    password = models.CharField(
        _('password'),
        max_length=128
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("User's status message")
    )
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Conversation(models.Model):
    """Model representing a conversation between users"""
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        verbose_name=_('participants')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated at')
    )

    class Meta:
        verbose_name = _('conversation')
        verbose_name_plural = _('conversations')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """Model representing a message in a conversation"""
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE,
        verbose_name=_('conversation')
    )
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE,
        verbose_name=_('sender')
    )
    message_body = models.TextField(verbose_name=_('message body'))
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('sent at')
    )
    read = models.BooleanField(
        default=False,
        verbose_name=_('read status')
    )

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['sent_at']

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"