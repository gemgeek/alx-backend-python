from rest_framework import viewsets, permissions, status  # type: ignore
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.response import Response  # type: ignore
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.generics import RetrieveAPIView
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination  
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return self.request.user.conversations.all()

    def create(self, request, *args, **kwargs):
        """
        Override create to handle conversation creation more explicitly
        and return a 201 CREATED status.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and sending messages within a specific conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation] 
    pagination_class = MessagePagination
    filterset_class = MessageFilter
    filter_backends = [DjangoFilterBackend] 

    def get_queryset(self):
        """
        This view should return a list of all messages for the conversation
        as determined by the URL, but only if the user is a participant.
        """
        conversation_pk = self.kwargs['conversation_pk']
        # Ensure the user is part of the conversation before showing messages
        return Message.objects.filter(
            conversation__conversation_id=conversation_pk,
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        """
        Assigns the sender (logged-in user) and conversation (from URL)
        automatically when creating a new message.
        """
        # 1. Get the conversation object from the database using the ID from the URL
        conversation = Conversation.objects.get(conversation_id=self.kwargs['conversation_pk'])
        
        # 2. Save the message, passing the full objects for sender and conversation
        serializer.save(sender=self.request.user, conversation=conversation)

class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]        
