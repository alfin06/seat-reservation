#Nick
from django.contrib import admin
from .models import ClassRoom, Seat, Reservation

admin.site.register(ClassRoom)
admin.site.register(Seat)
admin.site.register(Reservation)
