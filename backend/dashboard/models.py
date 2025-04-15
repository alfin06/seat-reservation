from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.
class Seat(models.Model):
    RESERVE_STATE = (
        (0, 'Reserved'),
        (1, 'Available'),
    )
    IS_DISABLE = (
        (0, 'Disable'),
        (1, 'Active')
    )
    id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(
        'ClassRoom',
        on_delete=models.CASCADE,
        related_name='seats',
        null=True,
        blank=True
    )
    seat_number = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    is_available = models.SmallIntegerField(choices=RESERVE_STATE, default=1)
    is_disable = models.SmallIntegerField(choices=IS_DISABLE, default=1)
    create_at = models.DateTimeField(default=timezone.now())
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        if not self.name:
            self.name = f"Seat {self.id} - {self.location}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Seat {self.id} - {self.location}"

class ClassRoom(models.Model):
    RESERVE_STATE = (
        (0, 'Reserved'),
        (1, 'Available'),
    )
    IS_DISABLE = (
        (0, 'Disable'),
        (1, 'Active')
    )
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    number_of_seats = models.IntegerField()
    is_available = models.SmallIntegerField(choices=RESERVE_STATE, default=1)
    is_disable = models.SmallIntegerField(choices=IS_DISABLE, default=1)
    create_at = models.DateTimeField(default=timezone.now())
    update_at = models.DateTimeField(auto_now=True)
        
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        if not self.name:
            self.name = f"Room {self.id} - {self.location}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room {self.id} - {self.location}"