from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.conf import settings

class User(AbstractUser):
    # Add extra fields here if needed
    # e.g.
    # phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """Model representing a conversation between users"""
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
        return f"Conversation {self.id}"

class Message(models.Model):
    """Model representing a message in a conversation"""
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
    content = models.TextField(verbose_name=_('content'))
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('timestamp')
    )
    read = models.BooleanField(
        default=False,
        verbose_name=_('read status')
    )

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"
