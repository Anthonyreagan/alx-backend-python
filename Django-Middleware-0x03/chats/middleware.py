# chats/middleware.py
from datetime import datetime, timedelta
from datetime import  time
from django.http import HttpResponseForbidden # Import HttpResponseForbidden for 403 responses
from collections import defaultdict




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
        allowed_start = time(7, 0)
        allowed_end = time(21,0)
        print(current_time)

        if current_time > allowed_end or current_time < allowed_start:
            return HttpResponseForbidden(
                "Accessing the messaging app is only allowed during 6 AM and 9 PM. "
            )

        response = self.getResponse(request)
        return response



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Storage format: {ip: {'count': int, 'window_start': datetime}}
        self.rate_limit_data = defaultdict(lambda: {'count': 0, 'window_start': datetime.now()})
        self.limit = 5  # 5 messages
        self.window = 60  # 60 seconds (1 minute)

    def __call__(self, request):
        # Only process POST requests to chat endpoints
        if request.method == 'POST' and request.path.startswith('/chat/'):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Get or initialize rate limit data for this IP
            data = self.rate_limit_data[ip]

            # Reset count if window has expired
            if (now - data['window_start']).seconds > self.window:
                data['count'] = 0
                data['window_start'] = now

            # Check and update count
            data['count'] += 1
            if data['count'] > self.limit:
                return HttpResponseForbidden(
                    "Message limit exceeded. Please wait before sending more messages."
                )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

from django.http import HttpResponseForbidden

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this chat.")
        return self.get_response(request)
