from django.urls import path
from .views import delete_user

urlpatterns = [
    path('users/delete/', delete_user, name='delete-user'),
]