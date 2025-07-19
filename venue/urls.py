from django.urls import path
from . import views


urlpatterns = [
    path("venues/", views.CreateAndGetVenues.as_view(), name="get-venues"),
    path("venues/slot/<int:venue_id>/",
         views.GetVenueSlot.as_view(), name="get-timeSlots"),
    path("venues/update/slot/<int:pk>/",
         views.UpdateVenueSlot.as_view(), name="update-venue-book"),
]
