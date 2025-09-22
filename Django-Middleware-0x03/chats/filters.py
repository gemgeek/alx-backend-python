import django_filters  # type: ignore
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Filter for messages sent within a date range
    timestamp = django_filters.DateFromToRangeFilter()

    # Filter by the user who sent the message
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'timestamp']