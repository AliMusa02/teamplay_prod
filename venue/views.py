from rest_framework import generics
from .serializer import VenueSerializer, VenueSlotsSerializer
from .models import VenueSlots, Venues
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

# VENUE APIS


class CreateAndGetVenues(generics.ListCreateAPIView):
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Venues.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admin can create venue")
        serializer.save()


class UpdateVenues(generics.UpdateAPIView):
    queryset = Venues.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admin can update")
        serializer.save()


# VENUE SLOTS APIS
class GetVenueSlot(generics.ListCreateAPIView):
    serializer_class = VenueSlotsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        venue_id = self.kwargs.get('venue_id')
        return VenueSlots.objects.select_related("venue").filter(
            venue_id=venue_id,
            is_booked=False
        )

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    # def perform_create(self, serializer):

    #     return super().perform_create(serializer)


class UpdateVenueSlot(generics.UpdateAPIView):
    queryset = VenueSlots.objects.all()
    serializer_class = VenueSlotsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if 'is_booked' not in request.data or len(request.data) != 1:
            raise PermissionDenied(
                "You can only update the 'is_booked' field.")

        return super().update(request, *args, **kwargs)
