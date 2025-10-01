from django.urls import path
from .views import delete_user, ThreadedMessagesView, UnreadMessagesView

urlpatterns = [
    path('users/delete/', delete_user, name='delete-user'),
    path('conversations/<int:pk>/threads/', ThreadedMessagesView.as_view(), name='threaded-messages'),
    path('messages/unread/', UnreadMessagesView.as_view(), name='unread-messages'),
]