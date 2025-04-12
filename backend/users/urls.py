from django.urls import path
from . import views
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

    path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/user', views.user, name='user'),
    path('api/register', views.register, name='register'),
]
