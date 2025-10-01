from django.contrib import admin
from .models import Message, Notification, MessageHistory

class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sender', 'receiver', 'is_edited', 'timestamp')

admin.site.register(Message, MessageAdmin)
admin.site.register(Notification)
admin.site.register(MessageHistory)
