from django.db.models.signals import post_save
from django.dispatch import receiver
from dashboard.models import *

@receiver(post_save, sender=ClassRoom)
def create_fixed_seats(sender, instance, created, **kwargs):
    if created:
        total = instance.number_of_seats

        for i in range(1, total + 1):
            Seat.objects.create(
                classroom=instance,
                location=instance.location
            )