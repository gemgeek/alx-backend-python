from django.http import HttpResponseForbidden
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"[{datetime.now()}] User: {user} - Path: {request.path}\n"

        # Log the message to a file
        with open("requests.log", "a") as log_file:
            log_file.write(log_message)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the allowed time range (9 AM to 6 PM)
        start_hour = 9
        end_hour = 18
        current_hour = datetime.now().hour

        # Check if the current hour is outside the allowed range
        if not (start_hour <= current_hour < end_hour):
            return HttpResponseForbidden("Access is restricted outside of 9 AM to 6 PM.")

        # If within the allowed time, proceed as normal
        response = self.get_response(request)
        return response    