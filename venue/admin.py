from django.contrib import admin
from .models import Venues, VenueSlots
# Register your models here.


@admin.register(Venues)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('created_at',)


@admin.register(VenueSlots)
class VenueSlotsAdmin(admin.ModelAdmin):
    list_display = ('id', 'venue', 'slot_time', 'is_booked', 'created_at')
    list_filter = ('venue', 'is_booked')
