from django.db.models.signals import post_save
from django.dispatch import receiver
from dashboard.models import *
import random

@receiver(post_save, sender=ClassRoom, dispatch_uid="create_fixed_seats_signal")
def create_fixed_seats(sender, instance, created, **kwargs):
    if created and instance.seats.count() == 0:
        total_seats = instance.number_of_seats
        seats_with_outlets = total_seats // 3
        
        seat_indices = list(range(total_seats))
        outlet_indices = random.sample(seat_indices, seats_with_outlets)
        
        seats = []
        for i in range(total_seats):
            has_outlet = i in outlet_indices
            seats.append(Seat(
                classroom=instance,
                location=instance.location,
                has_outlet=has_outlet
            ))
        
        Seat.objects.bulk_create(seats)