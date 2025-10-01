from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

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