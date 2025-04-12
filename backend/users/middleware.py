from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class CSRFExemptMiddleware(MiddlewareMixin):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Check if the path matches any of the exempt URLs
        path = request.path_info.lstrip('/')
        for exempt_url in settings.CSRF_EXEMPT_URLS:
            if path.startswith(exempt_url):
                setattr(request, '_dont_enforce_csrf_checks', True)
                return None
        return None 