from .models import Message
from .serializers import ThreadedMessageSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"result": "User deleted"}, status=status.HTTP_204_NO_CONTENT)

class ThreadedMessagesView(ListAPIView):
    serializer_class = ThreadedMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the conversation ID from the URL
        conversation_pk = self.kwargs['pk']

        # Build the optimized queryset
        queryset = Message.objects.filter(
            # Only get top-level messages (not replies)
            conversation_id=conversation_pk, 
            parent_message__isnull=True
        ).select_related(
            'sender'  # Use JOIN to fetch sender details
        ).prefetch_related(
            'replies' # Use a second query to fetch all replies efficiently
        ).order_by('timestamp')

        return queryset