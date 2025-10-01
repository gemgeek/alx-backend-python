from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user): 
        """
        Returns a queryset of unread messages for a given user.
        """
        return self.get_queryset().filter(
            receiver=user, 
            is_read=False
        )