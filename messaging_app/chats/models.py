import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    
    class Role(models.TextChoices):
        GUEST = 'GUEST', 'Guest'
        HOST = 'HOST', 'Host'
        ADMIN = 'ADMIN', 'Admin'

    # Using UUIDField for primary key to enhance security and uniqueness.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # This field stores the user's role using the choices we defined above.
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.GUEST)

    # A simple CharField for the phone number.
    # blank=True and null=True mean this field is optional.
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # auto_now_add=True automatically sets the timestamp when a user is first created.
    created_at = models.DateTimeField(auto_now_add=True)

    # AbstractUser already includes: username, first_name, last_name, email, password, etc.


class Conversation(models.Model):
    """
    Model to represent a conversation between two or more users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ManyToManyField allows multiple users to be part of a conversation.
    participants = models.ManyToManyField(User, related_name='conversations')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Model to represent a single message within a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ForeignKey links the message to the user who sent it.
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    # ForeignKey links the message to the conversation it belongs to.
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    # TextField is used for long-form text, perfect for a message body.
    message_body = models.TextField()

    # auto_now_add=True sets the timestamp when the message is created.
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"