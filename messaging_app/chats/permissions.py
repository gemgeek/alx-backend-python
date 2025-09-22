from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or view it.
    """
    def has_object_permission(self, request, view, obj):
        
        return obj.user == request.user
    
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated at the view level.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation object.
        'obj' here is an instance of the Conversation model.
        """
        # We assume your Conversation model has a ManyToManyField named 'participants'.
        return request.user in obj.participants.all()    