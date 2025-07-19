from django.db import models
from teams.models import Teams, TeamMember
from venue.models import Venues, VenueSlots
from datetime import date


# Create your models here.


class Invitation(models.Model):
    sender_team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name='sender_invitations', null=False, blank=False)
    receiver_team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name='receiver_invitations', null=False, blank=False)
    venue = models.ForeignKey(
        Venues, on_delete=models.CASCADE, related_name='invitations', null=False, blank=False)
    time_slot = models.TimeField(null=False, blank=False)
    date = models.DateField(default=date.today, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(("status"), max_length=50, default="pending")
    message = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"Invite from {self.sender_team} to {self.receiver_team} on {self.date} at {self.time_slot}"


class Matches(models.Model):
    home_team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, null=False, blank=False, related_name='away_matches')
    is_played = models.BooleanField(default=False)
    venue = models.ForeignKey(
        Venues, on_delete=models.CASCADE, related_name='matches')
    time_slot = models.OneToOneField(
        VenueSlots, on_delete=models.CASCADE, related_name='match')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.time_slot.date} at {self.time_slot.slot_time.strftime('%H:%M')}"
