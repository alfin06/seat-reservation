from dashboard.models import *
from rest_framework import serializers

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'classroom', 'seat_number', 'location', 'name', 'is_available', 'is_disable', 'create_at', 'update_at']
        read_only_fields = ['id', 'name', 'created_at', 'updated_at']
        extra_kwargs = {
            'is_available': {'required': False, 'default': 1},
            'is_disable': {'required': False, 'default': 1},
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

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'location', 'name', 'number_of_seats', 'is_available', 'is_disable']
        read_only_fields = ['id', 'location', 'name', 'number_of_seats', 'is_available']
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