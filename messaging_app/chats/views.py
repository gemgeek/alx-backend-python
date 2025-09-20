from rest_framework import viewsets, permissions, status  # type: ignore
from rest_framework.response import Response  # type: ignore
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    filterset_fields = ['conversation'] # Allows filtering messages by conversation ID

    def get_queryset(self):
        user_conversations = self.request.user.conversations.all()
        return Message.objects.filter(conversation__in=user_conversations)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
