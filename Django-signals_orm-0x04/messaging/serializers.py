from rest_framework import serializers
from .models import Message

# This serializer is for displaying replies *inside* a parent message.
# It avoids infinite nesting by not including its own 'replies' field.
class ReplySerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField() # Show username instead of ID

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'is_edited']

# This is the main serializer for top-level messages.
class ThreadedMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    # This line tells the serializer to use the ReplySerializer for the 'replies'
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'is_edited', 'replies']


class UnreadMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']        