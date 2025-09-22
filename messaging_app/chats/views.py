from rest_framework import viewsets, permissions,  # type: ignore
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.response import Response  # type: ignore
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.generics import RetrieveAPIView
from .permissions import IsParticipantOfConversation

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
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']

    def get_queryset(self):
        """
        This view should return a list of all messages for the
        conversation as determined by the nested URL.
        """
        # We get the conversation's primary key from the URL kwargs
        conversation_pk = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation_id=conversation_pk)

    def perform_create(self, serializer):
        # We also need to get the conversation from the URL to save the new message
        conversation_pk = self.kwargs['conversation_pk']
        serializer.save(
            sender=self.request.user,
            conversation_id=conversation_pk
        )

class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]        
