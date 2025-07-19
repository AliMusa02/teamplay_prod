from django.db import models
from datetime import date

# Create your models here.


class Venues(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            null=False, blank=False)
    location = models.CharField(max_length=400, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VenueSlots(models.Model):
    venue = models.ForeignKey(
        Venues, on_delete=models.CASCADE, related_name="time_slots")
    slot_time = models.TimeField()
    date = models.DateField(default=date.today)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('venue', 'date', 'slot_time')

    def __str__(self):
        return f"{self.venue.name} - {self.date} {self.slot_time.strftime('%H:%M')}"
