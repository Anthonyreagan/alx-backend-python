
from django.contrib import admin
from .models import User, Conversation, Message
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Conversation)
admin.site.register(Message)
