from django.contrib import admin
from .models import Conversation, InboxMessage


class InbosMessageAdmin(admin.ModelAdmin):
    readonly_fields = ['sender', 'conversation', 'body']


admin.site.register(Conversation)
admin.site.register(InboxMessage)
