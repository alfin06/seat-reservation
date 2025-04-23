from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.http import JsonResponse
from .views import (
    LoginView, 
    RegistrationView, 
    PasswordResetRequestView, 
    PasswordResetConfirmView,
    EmailVerificationView,
    LogoutView,
    UserProfileView
)

class GetCSRFToken(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"detail": "CSRF cookie set"})

urlpatterns = [
    path('auth/set-csrf-token/', ensure_csrf_cookie(GetCSRFToken.as_view()), name='set-csrf-token'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/user/', UserProfileView.as_view(), name='user_profile'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/verify-email/<str:token>/', EmailVerificationView.as_view(), name='email-verification'),
]
