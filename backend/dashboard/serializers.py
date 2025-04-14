from dashboard.models import *
from rest_framework import serializers

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'location', 'name', 'is_available', 'is_disable', 'create_at', 'update_at']
        read_only_fields = ['id', 'name', 'created_at', 'updated_at']
        extra_kwargs = {
            'is_available': {'required': False, 'default': 1},
            'is_disable': {'required': False, 'default': 1},
        }

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'location', 'name', 'number_of_seats', 'is_available', 'is_disable', 'create_at', 'update_at']
        read_only_fields = ['id', 'name', 'created_at', 'updated_at']
        extra_kwargs = {
            'is_available': {'required': False, 'default': 1},
            'is_disable': {'required': False, 'default': 1},
        }