# chats/middleware.py
from datetime import datetime
from datetime import  time
from django.http import HttpResponseForbidden # Import HttpResponseForbidden for 403 responses



class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user (authenticated or anonymous)
        user = request.user.username if request.user.is_authenticated else "Anonymous"

        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.getResponse = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        allowed_start = time(21, 0)
        allowed_end = time(6,0)
        print(current_time)

        if current_time > allowed_end or current_time < allowed_start:
            return HttpResponseForbidden(
                "Accessing the messaging app is only allowed during 6 AM and 9 PM. "
            )

        response = self.getResponse(request)
        return response

