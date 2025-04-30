from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .serializers import (
    LoginSerializer, 
    RegistrationSerializer, 
    UserSerializer, 
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .models import User, PasswordResetToken, EmailVerificationToken
import uuid
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

def all_user(request):
    return HttpResponse('Returning all users')

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # Comment out email verification check
            """
            if not user.email_verified_at:
                return Response(
                    {"error": "Please verify your email before logging in"},
                    status=status.HTTP_403_FORBIDDEN
                )
            """
            login(request, user)
            user.last_login = timezone.now()
            user.save()
            
            return Response({
                "message": "Login successful",
                "user": UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create verification token but don't send email for now
            token_obj = EmailVerificationToken.objects.create(user=user)
            
            # Automatically verify the email for testing
            #user.email_verified_at = timezone.now()
            user.save()

            # Comment out email sending for now
            
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{token_obj.token}"
            html_message = f'''
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">Welcome to Seat Reservation System!</h2>
                        <p>Hello {user.name},</p>
                        <p>Thank you for registering. Please verify your email address by clicking the button below:</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{verification_url}" 
                               style="background-color: #3498db; color: white; padding: 12px 25px; 
                                      text-decoration: none; border-radius: 5px; font-weight: bold;">
                                Verify Email Address
                            </a>
                        </div>
                        <p>Or copy and paste this link in your browser:</p>
                        <p style="background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
                            {verification_url}
                        </p>
                        <p>This link will expire in 24 hours.</p>
                        <p>Best regards,<br>Seat Reservation Team</p>
                    </div>
                </body>
            </html>
            '''
            try:
                send_mail(
                    subject='Verify your email - Seat Reservation System',
                    message=f'Please click the following link to verify your email: {verification_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                # logger.error(f"Failed to send verification email to {user.email}. Error: {str(e)}")
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            
            
            return Response({
                "message": "Registration successful. You can now log in.",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication required for password reset
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Create password reset token
                token_obj = PasswordResetToken.objects.create(user=user)
                
                # Create reset URL
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{token_obj.token}"
                
                # HTML email template
                html_message = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                            <h2 style="color: #2c3e50;">Reset Your Password</h2>
                            <p>Hello {user.name},</p>
                            <p>We received a request to reset your password. Click the button below to proceed:</p>
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{reset_url}" 
                                   style="background-color: #3498db; color: white; padding: 12px 25px; 
                                          text-decoration: none; border-radius: 5px; font-weight: bold;">
                                    Reset Password
                                </a>
                            </div>
                            <p>Or copy and paste this link in your browser:</p>
                            <p style="background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
                                {reset_url}
                            </p>
                            <p>This link will expire in 24 hours.</p>
                            <p>If you didn't request this, please ignore this email.</p>
                            <p>Best regards,<br>Seat Reservation Team</p>
                        </div>
                    </body>
                </html>
                """
                
                # Send password reset email
                send_mail(
                    'Reset Your Password - Seat Reservation System',
                    f'Click the following link to reset your password. This link is valid for 24 hours: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                return Response({
                    "message": "Password reset email has been sent. Please check your inbox/spam folder."
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # We return the same message even if the email doesn't exist for security
                return Response({
                    "message": "Password reset email has been sent. Please check your inbox/spam folder."
                }, status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Password has been reset successfully. You can now log in with your new password."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            # Get token object from database
            token_obj = EmailVerificationToken.objects.get(token=token)
            print(token_obj)
            
            if not token_obj.is_valid():
                return Response({
                    "error": "Verification link has expired. Please request a new one."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = token_obj.user
            if user.email_verified_at:
                return Response({
                    "message": "Email already verified."
                }, status=status.HTTP_200_OK)
            
            # Mark email as verified
            user.email_verified_at = timezone.now()
            user.save()
            
            # Mark token as used
            token_obj.is_used = True
            token_obj.save()
            
            return Response({
                "message": "Email verified successfully. You can now log in."
            }, status=status.HTTP_200_OK)
            
        except EmailVerificationToken.DoesNotExist:
            return Response({
                "error": "Invalid verification link."
            }, status=status.HTTP_400_BAD_REQUEST)
        

##############################
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm

@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({'message': 'CSRF cookie set'})

@require_http_methods(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        password = data['password']
    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'message': 'Invalid JSON'}, status=400
        )

    user = authenticate(request, username=email, password=password)

    if user:
        login(request, user)
        return JsonResponse({'success': True})
    return JsonResponse(
        {'success': False, 'message': 'Invalid credentials'}, status=401
    )

def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})

@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {'username': request.user.username, 'email': request.user.email}
        )
    return JsonResponse(
        {'message': 'Not logged in'}, status=401
    )

@require_http_methods(['POST'])
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    form = CreateUserForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response({
                "message": "Successfully logged out"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response({
                "error": "Failed to logout"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)