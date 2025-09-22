from django.urls import path, include  # type: ignore
from rest_framework_nested import routers  # type: ignore
from .views import ConversationViewSet, MessageViewSet

# The parent router for conversations
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# The nested router for messages within a conversation
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# The urlpatterns now include both the parent and nested routes.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]