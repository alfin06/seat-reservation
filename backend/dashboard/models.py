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
    HAS_OUTLET = (
        (0, 'No'),
        (1, 'Yes')
    )

    id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(
        'ClassRoom',
        on_delete=models.CASCADE,
        related_name='seats',
        null=True,
        blank=True
    )

    location = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    is_available = models.SmallIntegerField(choices=RESERVE_STATE, default=1)
    is_disable = models.SmallIntegerField(choices=IS_DISABLE, default=1)
    has_outlet = models.SmallIntegerField(choices=HAS_OUTLET, default=1)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.name:
            self.name = f"Seat - {self.location}"
        
        super().save(*args, **kwargs)

        if is_new and "Seat -" in self.name:
            self.name = f"Seat {self.id} - {self.location}"
            Seat.objects.filter(pk=self.pk).update(name=self.name)
#Nick   
class Reservation(models.Model):
    STATUS_CHOICES = (
        (0, 'Active'),
        (1, 'Completed'),
        (2, 'Cancelled'),
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reservations')
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE, related_name='reservations')
    seat = models.ForeignKey('Seat', on_delete=models.CASCADE, related_name='reservations')
    duration = models.PositiveIntegerField(default=1)  # in hours, max 4
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=0)
    reserved_at = models.DateTimeField(default=timezone.now)
    reserved_end= models.DateTimeField(default=timezone.now)
    create_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reservation by {self.student} for Seat {self.seat.id} in Room {self.classroom.id}"


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
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
        
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.name:
            self.name = f"Room {self.id} - {self.location}"
            self.__class__.objects.filter(pk=self.pk).update(name=self.name)

    def __str__(self):
        return f"Room {self.id} - {self.location}"