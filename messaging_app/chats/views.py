from rest_framework import viewsets, permissions  # type: ignore
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """
    
    serializer_class = ConversationSerializer
    
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the conversations
        for the currently authenticated user.
        """
    
        return self.request.user.conversations.all()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or created.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all messages in conversations
        that the current user is a part of.
        """
        
        user_conversations = self.request.user.conversations.all()
        return Message.objects.filter(conversation__in=user_conversations)

    def perform_create(self, serializer):
        """
        Automatically set the sender of a new message to the current user.
        """
        
        serializer.save(sender=self.request.user)
