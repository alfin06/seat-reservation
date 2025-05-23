from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets, permissions, generics
from rest_framework.decorators import action
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from dashboard.serializers import *
from users.serializers import UserSerializer
from dashboard.models import *
from users.models import User

# Create your views here.
#Nick
from django.core.mail import send_mail
from django.conf import settings
from dashboard.models import Reservation, Seat, ClassRoom
from dashboard.serializers import ReservationSerializer, SeatSerializer, ClassRoomSerializer

from datetime import timedelta
from django.utils import timezone
import pytz
# import qrcode
# from io import BytesIO

class ReservationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            duration = serializer.validated_data.get('duration', 1)
            if duration > 4:
                return Response({'error': 'Duration cannot exceed 4 hours.'}, status=400)
            reservation = serializer.save(user=request.user)
            # Send confirmation email
            # Convert UTC to Shanghai time
            
            html_message = f'''
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">Your Seat Reservation Has Been Confirmed!</h2>
                        <p>Hello {request.user.name},</p>
                        <p>Your seat reservation has been confirmed. Here is the detail of your reservation:</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <p><strong>Classroom:</strong> {reservation.classroom.name}</p>
                            <p><strong>Seat:</strong> Seat {reservation.seat.id}</p>
                            <p><strong>Start time:</strong> {reservation.reserved_at}</p>
                            <p><strong>End time:</strong> {reservation.reserved_end}</p>
                        </div>
                        <p><i>Disclaimer: This is an automated email. Please do not reply to this email.</i></p>
                        <p>Best regards,<br>Seat Reservation Team</p>
                    </div>
                </body>
            </html>
            '''

            try:
                send_mail(
                    subject='Seat Reservation Confirmation',
                    message=f"Your reservation for seat {reservation.seat.id} in room {reservation.classroom.id} is confirmed.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception as e:
                return Response({'error': 'Reservation failed!'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(ReservationSerializer(reservation).data, status=201)
        return Response(serializer.errors, status=400)

class AvailableRoomsSeatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # has_outlet = request.query_params.get('has_outlet')
        rooms = ClassRoom.objects.filter(is_available=1, is_disable=1)
        data = []

        for room in rooms:
            seats_qs = room.seats.filter(is_available=1, is_disable=1)
            # if has_outlet is not None:
            #     seats_qs = seats_qs.filter(has_outlet=(has_outlet.lower() == 'true'))

            room_data = ClassRoomSerializer(room).data
            room_data['seats'] = SeatSerializer(seats_qs, many=True).data
            data.append(room_data)

        return Response({'rooms': data})

##Nick

class AdminDashboardStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        total_seats = Seat.objects.count()
        empty_seats_count = Seat.objects.filter(is_available=False).count()
        available_seats_count = total_seats - empty_seats_count
        total_classrooms = ClassRoom.objects.count()
        empty_classroom_count = ClassRoom.objects.filter(is_available=False).count()
        available_classroom_count = total_classrooms - empty_classroom_count
        number_of_user = User.objects.count()

        data = {
            "total_seats": total_seats,
            "empty_seats_count": empty_seats_count,
            "available_seats_count": available_seats_count,
            "total_classrooms": total_classrooms,
            "empty_classroom_count": empty_classroom_count,
            "available_classroom_count": available_classroom_count,
            "number_of_user": number_of_user,
        }

        return Response(data)

class AdminDashboardRoomsStats(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, format=None):
        classrooms = ClassRoom.objects.all()
        serializer = ClassRoomSerializer(classrooms, many=True)
        return Response(serializer.data)

class AdminDashboardUserStats(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class SeatGetAll(APIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [IsAdminUser, TokenAuthentication]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, format=None):
        try:
            queryset = Seat.objects.all().order_by('update_at')
            seats_data = []
            for seat in queryset:
                seats_data.append({
                    'id': seat.id,
                    'name': seat.name,
                    'location': seat.location,
                    'is_available': {
                        'value': seat.is_available,
                        'display': seat.get_is_available_display()
                    },
                    'classroom': seat.classroom.name,
                    'has_outlet': {
                        'value': seat.has_outlet,
                        'display': seat.get_has_outlet_display()
                    },
                    'is_disable': {
                        'value': seat.is_disable,
                        'display': seat.get_is_disable_display()
                    },
                    'update_at': seat.update_at.strftime("%Y-%m-%d %H:%M:%S")
                })
            
            return JsonResponse({
                'status': 'success',
                'count': len(seats_data),
                'data': seats_data
            }, safe=False)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Failed to fetch seats: {str(e)}"
            }, status=500)

class SeatDisableView(APIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [IsAdminUser, TokenAuthentication]
    authentication_classes = [TokenAuthentication]

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def post(self, request, format=None):
        seat_id = request.data.get('id')
        if not seat_id:
            return Response({'error': 'Missing seat id.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            seat = Seat.objects.get(pk=seat_id)
        except Seat.DoesNotExist:
            return Response({'error': f'Seat with id {seat_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        seat.is_disable = 0
        seat.save()

        return Response({'message': f'Seat {seat_id} has been disable successfully.'},
                        status=status.HTTP_201_CREATED)

class SeatEnableView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def post(self, request, format=None):
        seat_id = request.data.get('id')
        if not seat_id:
            return Response({'error': 'Missing seat id.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            seat = Seat.objects.get(pk=seat_id)
        except Seat.DoesNotExist:
            return Response({'error': f'Seat with id {seat_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if seat.classroom and seat.classroom.is_disable == 0:
            return Response(
                {'error': 'Cannot enable this seat because its classroom is disabled.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        seat.is_disable = 1
        seat.save()

        return Response({'message': f'Seat {seat_id} has been enable successfully.'},
                        status=status.HTTP_201_CREATED)

class ClassRoomGetAll(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        try:
            queryset = ClassRoom.objects.all().order_by('update_at')
            classrooms_data = []
            for classroom in queryset:
                classrooms_data.append({
                    'id': classroom.id,
                    'name': classroom.name,
                    'location': classroom.location,
                    'number_of_seat': classroom.number_of_seats,
                    'is_available': {
                        'value': classroom.is_available,
                        'display': classroom.get_is_available_display()
                    },
                    'is_disable': {
                        'value': classroom.is_disable,
                        'display': classroom.get_is_disable_display()
                    },
                    'updated_at': classroom.update_at.strftime("%Y-%m-%d %H:%M:%S")
                })
            
            return JsonResponse({
                'status': 'success',
                'count': len(classrooms_data),
                'data': classrooms_data
            }, safe=False)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Failed to fetch seats: {str(e)}"
            }, status=500)

class ClassRoomCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['location'] = self.kwargs.get('location')
        return context

    def create(self, request, *args, **kwargs):
        location = self.kwargs.get('location')
        if location:
            request.data['location'] = location
        return super().create(request, *args, **kwargs)

    def get(self):
        return Response({"detail": "Use POST to create a seat."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ClassRoomDisableView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    
    def post(self, request, format=None):
        classroom_id = request.data.get('id')
        if not classroom_id:
            return Response({'error': 'Missing classroom id.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            classroom = ClassRoom.objects.get(pk=classroom_id)
        except ClassRoom.DoesNotExist:
            return Response({'error': f'ClassRoom with id {classroom_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        classroom.is_disable = 0
        classroom.save()

        classroom.seats.update(is_disable=0)

        return Response({'message': f'ClassRoom {classroom_id} and its seats have been disabled successfully.'},
                        status=status.HTTP_201_CREATED)
    
class ClassRoomEnableView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

    def post(self, request, format=None):
        classroom_id = request.data.get('id')
        if not classroom_id:
            return Response({'error': 'Missing classroom id.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            classroom = ClassRoom.objects.get(pk=classroom_id)
        except ClassRoom.DoesNotExist:
            return Response({'error': f'ClassRoom with id {classroom_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        classroom.is_disable = 1
        classroom.save()

        classroom.seats.update(is_disable=1)

        return Response({'message': f'ClassRoom {classroom_id} and its seats have been enable successfully.'},
                        status=status.HTTP_201_CREATED)

class ReservationSettingUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReservationSettingSerializer

    def get_object(self):
        return ReservationSetting.get_solo()

    def update(self, request, *args, **kwargs):
        # Treat PUT like PATCH to allow partial updates
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class ReservationSettingView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSettingSerializer

    def get(self, request, format=None):
        try:
            queryset = ReservationSetting.objects.all()
            setting_data = []
            for data in queryset:
                setting_data.append({
                    'max_booking_duration': data.max_booking_duration,
                })
            
            return JsonResponse({
                'status': 'success',
                'data': setting_data
            }, safe=False)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Failed to fetch settings: {str(e)}"
            }, status=500)

class InstantBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seat_id = request.data.get('seat_id')
        try:
            duration = int(request.data.get('duration', 1))
        except (TypeError, ValueError):
            return Response({'error': 'Invalid duration'}, status=400)

        # 1. Validate seat
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            return Response({'error': 'Seat not found'}, status=404)
        if not seat.is_available or seat.is_disable == 0:
            return Response({'error': 'Seat is not available'}, status=400)

        # 2. Validate duration
        if duration < 1 or duration > 4:
            return Response({'error': 'Duration must be between 1 and 4 hours'}, status=400)

        # 3. Check for overlapping reservations
        # Get current time in UTC and convert it to Shanghai time
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        now_utc = timezone.now()
        now = now_utc.astimezone(shanghai_tz)  # Current time in Shanghai timezone

        end_time = now + timedelta(hours=duration)

        overlapping = Reservation.objects.filter(
            seat=seat,
            status__in=['0', '1'],  # Active or Checked-In
            reserved_at__lt=end_time,
            reserved_end__gt=now
        ).exists()
        if overlapping:
            return Response({'error': 'Seat is already reserved for this time period'}, status=400)

        # 4. Create reservation
        reservation = Reservation.objects.create(
            user=request.user,
            classroom=seat.classroom,
            seat=seat,
            duration=duration,
            reserved_at=now,
            reserved_end=end_time,
            status='1'  # Checked-In
        )

        # 5. Update seat status
        seat.is_available = 0
        seat.save()

        # 6. Return reservation details
        return Response({
            'reservation_id': reservation.id,
            'seat_id': seat.id,
            'seat_name': seat.name,
            'classroom': seat.classroom.name,
            'location': seat.location,
            'duration': reservation.duration,
            'status': 'CHECKED-IN',
            'reserved_at': reservation.reserved_at,
            'reserved_end': reservation.reserved_end
        }, status=201)
    
class QRCodeCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        seat_id = request.data.get('qrCode')  # Assuming QR code carries seat ID

        if not user_id or not seat_id:
            return Response({"detail": "Missing user_id or qrCode"}, status=status.HTTP_400_BAD_REQUEST)

        # Get current time in UTC and convert it to Shanghai time
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        now_utc = timezone.now()
        now = now_utc.astimezone(shanghai_tz)  # Current time in Shanghai timezone

        # Filter potential matching reservations
        reservations = Reservation.objects.filter(
            user__id=user_id,
            seat__id=seat_id,
            status=0  # Only active reservations
        )

        for reservation in reservations:
            checkin_window_start = reservation.reserved_at - timedelta(minutes=10)

            if checkin_window_start <= now <= reservation.reserved_end:
                reservation.status = 1  # Checked-In
                reservation.checked_in_at = now
                reservation.save()
                return Response({"detail": "Checked in successfully. "}, status=201)

        return Response({"detail": "No valid reservation for check-in found."}, status=400)

class QRCodeCheckView2(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seat_id = request.data.get('seat_id')
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            return Response({'error': 'Seat not found'}, status=404)

        if not seat.is_available or seat.is_disable == 0:
            return Response({'error': 'Seat is not available'}, status=400)

        return Response({
            'seat_id': seat.id,
            'seat_name': seat.name,
            'classroom': seat.classroom.name,
            'location': seat.location
        })

# Commenting out QR code generation since we're not using it
# class GenerateQRCodeView(APIView):
#     permission_classes = [IsAuthenticated]
# 
#     def get(self, request, seat_id):
#         try:
#             seat = Seat.objects.get(id=seat_id)
#         except Seat.DoesNotExist:
#             return Response({'error': 'Seat not found'}, status=404)
# 
#         # Create QR code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(str(seat.id))
#         qr.make(fit=True)
# 
#         # Create image
#         img = qr.make_image(fill_color="black", back_color="white")
#         
#         # Save to BytesIO
#         buffer = BytesIO()
#         img.save(buffer, format='PNG')
#         buffer.seek(0)
# 
#         # Return as response
#         response = HttpResponse(buffer.getvalue(), content_type='image/png')
#         response['Content-Disposition'] = f'attachment; filename="seat_{seat_id}_qr.png"'
#         return response

class UserReservationStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=user_id)

            total = Reservation.objects.filter(user=user).count()
            active = Reservation.objects.filter(user=user, status='0').count()
            completed = Reservation.objects.filter(user=user, status='1').count()
            cancelled = Reservation.objects.filter(user=user, status='2').count()

            return Response({
                "total_reservations": total,
                "active_reservations": active,
                "completed_reservations": completed,
                "cancelled_reservations": cancelled,
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ActiveReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=user_id)

            # Get the active reservations for the user, ordered by reserved_at
            reservations = Reservation.objects.filter(user=user, status='0').order_by('reserved_at')

            # Manually prepare the data to return
            active_reservations = [
                {
                    "id": reservation.id,
                    "classroom": reservation.classroom.name,
                    "seat_id": reservation.seat.id,
                    "reserved_start_time": reservation.reserved_at,
                    "reserved_end_time": reservation.reserved_end,
                    "status": reservation.status,
                }
                for reservation in reservations
            ]

            return Response(active_reservations, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CancelReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        user = request.user

        try:
            reservation = Reservation.objects.get(id=reservation_id)

            # if reservation.user != user and not user.is_staff:
            #     return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

            # if reservation.status == "CANCELLED":
            #     return Response({"message": "Reservation already cancelled."}, status=status.HTTP_200_OK)

            reservation.status = 2
            reservation.save()

            return Response({"message": "Reservation cancelled successfully."}, status=status.HTTP_200_OK)

        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)
        
class UpdateClassroomView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            classroom_id = request.data.get('id')
            if not classroom_id:
                return Response({'message': 'Missing classroom ID'}, status=status.HTTP_400_BAD_REQUEST)

            classroom = ClassRoom.objects.filter(id=classroom_id).first()
            if not classroom:
                return Response({'message': 'Classroom not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ClassRoomSerializer(classroom, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Classroom updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Validation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': f'Server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)