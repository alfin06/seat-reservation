from django.urls import path
from .views import (
    LoginView, 
    RegistrationView, 
    PasswordResetRequestView, 
    PasswordResetConfirmView,
    EmailVerificationView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('verify-email/<str:token>/', EmailVerificationView.as_view(), name='email-verification'),
]

