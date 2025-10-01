from django.urls import path
from .views import DeleteUserView

urlpatterns = [
    path('users/delete/', DeleteUserView.as_view(), name='delete-user'),
]