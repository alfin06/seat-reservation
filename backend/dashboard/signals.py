from django.db.models.signals import post_save
from django.dispatch import receiver
from dashboard.models import *

@receiver(post_save, sender=ClassRoom, dispatch_uid="create_fixed_seats_signal")
def create_fixed_seats(sender, instance, created, **kwargs):
    if created and instance.seats.count() == 0:
        Seat.objects.bulk_create([
            Seat(classroom=instance, location=instance.location)
            for i in range(instance.number_of_seats)
        ])