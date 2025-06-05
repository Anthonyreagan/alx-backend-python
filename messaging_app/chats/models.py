from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings  # For referencing AUTH_USER_MODEL in relations

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Add additional fields here if needed.
    """
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
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # Using settings.AUTH_USER_MODEL here
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
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Conversation')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Using settings.AUTH_USER_MODEL here
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('Sender')
    )
    text = models.TextField(
        verbose_name=_('Message Text')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Timestamp')
    )
    read = models.BooleanField(
        default=False,
        verbose_name=_('Read Status')
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['timestamp']

    def __str__(self):
        return f"Message {self.id} from {self.sender}"