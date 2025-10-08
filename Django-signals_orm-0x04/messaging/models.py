from django.db import models
from django.conf import settings
from .managers import UnreadMessagesManager

User = settings.AUTH_USER_MODEL

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name='replies', 
        on_delete=models.CASCADE
    )
    # Attach the managers
    objects = models.Manager() 
    unread = UnreadMessagesManager() 

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message {self.message.id} at {self.edited_at:%Y-%m-%d %H:%M}"    

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"
