from rest_framework import serializers  # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    
    role = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['sender', 'conversation']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model with custom fields and validation.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'message_count']

    def get_message_count(self, obj):
        return obj.messages.count()

    def validate(self, data):
        """
        Check that a conversation is created with at least two participants.
        """
        participants = self.context['request'].data.get('participants')
        if not participants or len(participants) < 2:
            # THIS IS THE ONLY LINE THAT CHANGES
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data