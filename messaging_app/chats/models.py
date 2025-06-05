from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True
    )
    password = models.CharField(
        _('password'),
        max_length=128
    )  # Explicit password field
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        verbose_name=_('Profile Picture')
    )
    status = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Status')
    )
    last_online = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Online')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Model representing a conversation between users.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name=_('Participants')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Conversation')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('Sender')
    )
    message_body = models.TextField(
        verbose_name=_('Message Body')
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Sent At')
    )
    read = models.BooleanField(
        default=False,
        verbose_name=_('Read Status')
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['sent_at']

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"