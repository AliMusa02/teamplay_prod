from rest_framework import serializers
from .models import Matches, Invitation
from venue.models import Venues, VenueSlots
from teams.models import Teams


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venues
        fields = ['id', 'name', 'location']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueSlots
        fields = ['id', 'slot_time', 'date', 'is_booked', 'created_at']


class teamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['id', 'team_name', 'team_logo', 'captain']


class InvitationSerializer(serializers.ModelSerializer):
    receiver_team_id = serializers.PrimaryKeyRelatedField(
        queryset=Teams.objects.all(), write_only=True, source="receiver_team"
    )
    sender_team = teamSerializer(read_only=True)
    receiver_team = teamSerializer(read_only=True)

    time_slot = serializers.TimeField()
    date = serializers.DateField()
    message = serializers.CharField()

    # venue_detail = VenueSerializer(read_only=True)
    # venue = serializers.PrimaryKeyRelatedField(queryset=Venues.objects.all())
    venue = VenueSerializer(read_only=True)   # ✅ for GET
    venue_id = serializers.PrimaryKeyRelatedField(  # ✅ for POST
        queryset=Venues.objects.all(), write_only=True, source='venue'
    )

    class Meta:
        model = Invitation
        fields = ['id', 'status', 'message', 'sender_team', 'receiver_team', 'receiver_team_id', "time_slot", "date", "message",
                  'venue', 'venue_id', 'created_at']


class MatchesSerializer(serializers.ModelSerializer):
    # sender_teamId = serializers.IntegerField(
    #     source='home_team.id', read_only=True)
    # sender_teamName = serializers.CharField(
    #     source='home_team.team_name', read_only=True)
    home_team_captainId = serializers.IntegerField(
        source="home_team.captain.id", read_only=True)

    # receiver_teamId = serializers.IntegerField(
    #     source='away_team.id', read_only=True)
    # receiver_teamName = serializers.CharField(
    #     source='away_team.team_name', read_only=True)
    away_team_captainId = serializers.CharField(
        source='away_team.captain.id', read_only=True)

    home_team = teamSerializer(read_only=True)
    away_team = teamSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)

    class Meta:
        model = Matches
        fields = ['id', 'is_played', 'created_at', 'home_team', 'home_team_captainId', 'away_team', 'away_team_captainId',
                  'venue', 'time_slot']
