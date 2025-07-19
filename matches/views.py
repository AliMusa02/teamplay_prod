from django.shortcuts import render
from rest_framework import generics, status
from .serializer import InvitationSerializer, MatchesSerializer
from .models import Invitation, Matches
from rest_framework.permissions import IsAuthenticated, AllowAny
from teams.models import Teams
from venue.models import VenueSlots, Venues
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.exceptions import NotFound
from django.db.models import Q

# Create your views here.


class CreateAndGetInvitations(generics.ListCreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if Teams.objects.filter(captain=user).exists():
            return Invitation.objects.filter(receiver_team__captain=user, status="pending")

        return Invitation.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        receiver_team = serializer.validated_data.get("receiver_team")
        venue = serializer.validated_data.get("venue")
        time_slot = serializer.validated_data.get("time_slot")
        date = serializer.validated_data.get("date")
        message = serializer.validated_data.get("message")

        user = self.request.user
        receiver_team = serializer.validated_data.get("receiver_team")

        if not receiver_team:
            raise PermissionDenied("receiver id cannot be null")
        try:
            sender_team = Teams.objects.get(captain=user)
        except Teams.DoesNotExist:
            raise PermissionDenied('Only captains can send invitations')

        if sender_team == receiver_team:
            raise PermissionDenied(
                "You cannot send an invitation to your own team")

        if Invitation.objects.filter(venue=venue, time_slot=time_slot, date=date).exists():
            raise PermissionDenied(
                "This venue is already booked at the selected time and date")

        serializer.save(sender_team=sender_team,
                        receiver_team=receiver_team,
                        venue=venue,
                        time_slot=time_slot,
                        date=date,
                        message=message
                        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Invitation sent successfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = request.user

        try:
            team = Teams.objects.get(captain=user)
        except Teams.DoesNotExist:
            return Response({
                "message": "Only captains can view invitations.",
                "data": []
            }, status=status.HTTP_403_FORBIDDEN)

        queryset = Invitation.objects.filter(
            receiver_team=team, status="pending")
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Pending invitations fetched successfully" if queryset else "No pending invitations yet.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

        # return Response({
        #     "message": "Pending invitations fetched successfully",
        #     "data": serializer.data
        # })


class UpdateInvitation(generics.UpdateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        user = request.user
        invitation = self.get_object()

        if invitation.receiver_team.captain != user:
            raise PermissionDenied(
                "Only invited  team captain's can update this invitation")

        new_status = request.data.get('status')
        if new_status not in ["accepted", "declined", "pending"]:
            return Response({"error": "Invalid status. Must be 'accepted' or 'declined' "}, status=status.HTTP_400_BAD_REQUEST)

        invitation.status = new_status
        invitation.save()

        if new_status == "accepted":
            existing_slot = VenueSlots.objects.filter(
                venue=invitation.venue,
                date=invitation.date,
                slot_time=invitation.time_slot
            ).first()

            if existing_slot and existing_slot.is_booked:
                return Response({"error": "The selected slot is already booked."}, status=status.HTTP_400_BAD_REQUEST)

            if existing_slot:
                existing_slot.is_booked = True
                existing_slot.save()
                slot_to_use = existing_slot

            else:
                slot_to_use = VenueSlots.objects.create(
                    venue=invitation.venue,
                    date=invitation.date,
                    slot_time=invitation.time_slot,
                    is_booked=True
                )

            match = Matches.objects.create(
                home_team=invitation.sender_team,
                away_team=invitation.receiver_team,
                venue=invitation.venue,
                time_slot=slot_to_use
            )

        return Response({
            "message": f"Invitation successfully {new_status}.",
            "status": new_status,
            "match_id": match.id
        }, status=status.HTTP_200_OK)


class GetAllinvitations(generics.ListAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [AllowAny]


class GetAllMatches(generics.ListAPIView):
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer
    permission_classes = [IsAuthenticated]


class GetOwnMatches(generics.ListAPIView):
    serializer_class = MatchesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        team_id = self.kwargs.get("team_id")

        if not team_id:
            raise NotFound("Please provide a team ID.")

        try:
            team = Teams.objects.get(id=team_id)
        except Teams.DoesNotExist:
            raise NotFound("Team not found.")

        if not (team.captain == user or team.members.filter(user=user).exists()):
            raise PermissionDenied("You are not part of this team.")

        return Matches.objects.filter(Q(home_team=team) | Q(away_team=team))
