from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets, permissions, generics
from rest_framework.decorators import action
from django.utils import timezone
from django.http import JsonResponse
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

        # Remove timezone info from 'now' for comparison
        now_naive = now.replace(tzinfo=None)

        # Filter potential matching reservations
        reservations = Reservation.objects.filter(
            user__id=user_id,
            seat__id=seat_id,
            status=0  # Only active reservations
        )

        for reservation in reservations:
            reserved_at_naive = reservation.reserved_at.replace(tzinfo=None)
            reserved_end_naive = reservation.reserved_end.replace(tzinfo=None)
            checkin_window_start = reserved_at_naive - timedelta(minutes=10)

            if checkin_window_start <= now_naive <= reserved_end_naive:
                reservation.status = 1  # Checked-In
                reservation.save()
                return Response({"detail": "Checked in successfully. "}, status=201)

        return Response({"detail": "No valid reservation for check-in found."}, status=400)