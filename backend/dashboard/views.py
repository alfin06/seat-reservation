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
            # Send confirmation email (simple example)
            try:
                send_mail(
                    subject='Seat Reservation Confirmation',
                    message=f"Your reservation for seat {reservation.seat.id} in room {reservation.classroom.id} is confirmed.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                pass  # Optionally log error
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
    serializer_class = ReservationResetSettingSerializer

    def get_object(self):
        return ReservationSetting.get_solo()

    
    def update(self, request, *args, **kwargs):
        # Treat PUT just like PATCH → only the provided fields get updated.
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class ReservationSettingView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationResetSettingSerializer

    def get(self, request, format=None):
        try:
            queryset = ReservationSetting.objects.all()
            setting_data = []
            for data in queryset:
                setting_data.append({
                    'max_booking_duration': data.max_booking_duration,
                    'reset_time': data.reset_time
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
        now = timezone.now()
        end_time = now + timedelta(hours=duration)
        overlapping = Reservation.objects.filter(
            seat=seat,
            status__in=['0', '3'],  # Active or Checked-In
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
            status='3'  # Checked-In
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