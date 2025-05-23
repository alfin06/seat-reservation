from dashboard.models import *
from rest_framework import serializers
from django.utils.timezone import localtime
import datetime

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        #Nick
        fields = ['id', 'classroom', 'location', 'name', 'is_available', 'is_disable', 'has_outlet', 'create_at', 'update_at']
        read_only_fields = ['id', 'name', 'created_at', 'updated_at']
        extra_kwargs = {
            'is_available': {'required': False, 'default': 1},
            'is_disable': {'required': False, 'default': 1},
            'has_outlet': {'required': False, 'default': 1},
        }
         
    def validate(self, data):
        classroom = data.get('classroom')
        seat_number = data.get('seat_number')
        
        if classroom and seat_number:
            instance_id = self.instance.id if self.instance else None
            query = Seat.objects.filter(
                classroom=classroom,
                seat_number=seat_number
            )
            if instance_id:
                query = query.exclude(id=instance_id)
                
            if query.exists():
                raise serializers.ValidationError({
                    "seat_number": f"Seat number {seat_number} already exists in this classroom."
                })
        
        return data

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'classroom', 'seat', 'duration', 'status', 'reserved_at', 'reserved_end']
        read_only_fields = ['id', 'status']

class ReservationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationSetting
        fields = ['max_booking_duration']
        extra_kwargs = {
            'max_booking_duration': {'required': False},
        }
    
    def update(self, instance, validated_data):
        # Only update fields that are provided in the request
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "You must provide at least one of: max_booking_duration or reset_time."
            )
        return attrs

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'location', 'name', 'number_of_seats', 'is_available', 'is_disable', 'create_at', 'update_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'is_available': {'required': False, 'default': 1},
            'is_disable': {'required': False, 'default': 1},
        }

    def get_seat_count(self, obj):
        return obj.seats.count()

    def validate_number_of_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of seats must be greater than zero.")
        return value
    
    def validate_location(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Location cannot be empty.")
        return value