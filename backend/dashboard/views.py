from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status, viewsets, permissions, generics
from django.conf import settings
from django.utils import timezone
from dashboard.serializers import *
from users.serializers import UserSerializer
from dashboard.models import *
from users.models import User

# Create your views here.
class AdminDashboardStatusView(APIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]

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
    permission_classes = [AllowAny]  # Temporary for testing
    # permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, format=None):
        classrooms = ClassRoom.objects.all()
        serializer = ClassRoomSerializer(classrooms, many=True)
        return Response(serializer.data)

class AdminDashboardUserStats(APIView):
    permission_classes = [AllowAny]  # Temporary for testing
    # permission_classes = [IsAdminUser]    

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class SeatCreateView(generics.CreateAPIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_serializer_context(self):
        # Pass location from URL to the serializer context if needed.
        context = super().get_serializer_context()
        context['location'] = self.kwargs.get('location')
        return context

    def create(self, request, *args, **kwargs):
        # If location is passed via URL, add it to the request data.
        location = self.kwargs.get('location')
        if location:
            request.data['location'] = location
        return super().create(request, *args, **kwargs)

    def get(self):
        return Response({"detail": "Use POST to create a seat."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SeatDisableView(generics.DestroyAPIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def post(self, request, format=None):
        seat_id = request.data.get('id')
        if not seat_id:
            return Response({"detail": "Seat id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seat = Seat.objects.get(id=seat_id)
            seat.is_disable = 0
            seat.save(update_fields=['is_disable', 'updated_at'])
            return Response({"detail": "Seat disable successfully."}, status=status.HTTP_201_CREATED)
        except Seat.DoesNotExist:
            return Response({"detail": "Seat not found."}, status=status.HTTP_404_NOT_FOUND)

class SeatEnableView(generics.DestroyAPIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def post(self, request, format=None):
        seat_id = request.data.get('id')
        if not seat_id:
            return Response({"detail": "Seat id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seat = Seat.objects.get(id=seat_id)
            seat.is_disable = 1
            seat.save(update_fields=['is_disable', 'updated_at'])
            return Response({"detail": "Seat enable successfully."}, status=status.HTTP_201_CREATED)
        except Seat.DoesNotExist:
            return Response({"detail": "Seat not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ClassRoomCreateView(generics.CreateAPIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]
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
    # permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

    def post(self, request, format=None):
        classroom_id = request.data.get('id')
        if not classroom_id:
            return Response({"detail": "ClassRoom id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            classroom = ClassRoom.objects.get(id=classroom_id)
            classroom.is_disable = 0
            classroom.save(update_fields=['is_disable', 'updated_at'])
            return Response({"detail": "ClassRoom disable successfully."}, status=status.HTTP_201_CREATED)
        except ClassRoom.DoesNotExist:
            return Response({"detail": "ClassRoom not found."}, status=status.HTTP_404_NOT_FOUND)

class ClassRoomEnableView(generics.DestroyAPIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

    def post(self, request, format=None):
        classroom_id = request.data.get('id')
        if not classroom_id:
            return Response({"detail": "ClassRoom id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            classroom = ClassRoom.objects.get(id=classroom_id)
            classroom.is_disable = 1
            classroom.save(update_fields=['is_disable', 'updated_at'])
            return Response({"detail": "ClassRoom enable successfully."}, status=status.HTTP_201_CREATED)
        except ClassRoom.DoesNotExist:
            return Response({"detail": "ClassRoom not found."}, status=status.HTTP_404_NOT_FOUND)
        