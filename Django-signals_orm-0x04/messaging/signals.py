from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.db.models import Q
from .models import Message, Notification, MessageHistory
User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before a message is saved, check if its content has changed.
    """
    # We only care about edits, not new messages being created.
    # If 'instance.pk' is None, it means the object is new.
    if instance.pk:
        try:
            # Get the original message from the database
            original_message = Message.objects.get(pk=instance.pk)

            # Compare the original content with the new content
            if original_message.content != instance.content:
                # If it changed, create a history record with the old content
                MessageHistory.objects.create(
                    message=original_message,
                    old_content=original_message.content
                )
                # Mark the message instance as edited
                instance.is_edited = True
        except Message.DoesNotExist:
            # This case happens on the very first save of a new message.
            # We can safely ignore it.
            pass 


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Deletes all messages and notifications related to a user
    after their account is deleted.
    """
    # Note: on_delete=CASCADE handles this at the DB level.
    # This signal is for demonstration and custom logic.

    print(f"Signal received: Cleaning up data for deleted user {instance.username}")

    # Delete messages where the user was the sender OR the receiver
    Message.objects.filter(Q(sender=instance) | Q(receiver=instance)).delete()

    # The related notifications and message histories will be deleted automatically
    # by the CASCADE effect from deleting the messages.               