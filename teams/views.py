
from rest_framework import generics
from .serializer import TeamSerializer, TeamMemberSerializer
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


from .models import Teams, TeamMember
# Create your views here.


# TEAM GET,CREATE,DELETE AND UPDATE APIS

class CreateAndGetTeams(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            user_team = TeamMember.objects.get(user=user).team
            return Teams.objects.exclude(id=user_team.id).select_related('captain')
        except TeamMember.DoesNotExist:
            return Teams.objects.select_related('captain').all()

    def perform_create(self, serializer):
        user = self.request.user

        if TeamMember.objects.filter(user=user).exists():
            raise PermissionDenied(
                "You are already in a team and cannot create another.")

        if Teams.objects.filter(team_name=serializer.validated_data['team_name']).exists():
            raise PermissionDenied("A team with this name already exists.")

        team = serializer.save(captain=user)
        TeamMember.objects.create(user=user, team=team, role="captain")


class deleteTeam(generics.DestroyAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Teams.objects.filter(captain=self.request.user)

    def get_object(self):
        team = super().get_object()
        if team.captain != self.request.user:
            raise PermissionDenied("You cannot delete someone else's team.")
        return team

    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        response = super().delete(request, *args, **kwargs)
        return Response({"message": "Team successfully deleted"}, status=status.HTTP_200_OK)


class getOneTeam(generics.RetrieveAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class updateTeam(generics.UpdateAPIView):
    # queryset = Teams.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Teams.objects.filter(captain=self.request.user)

    def get_object(self):
        try:
            team = super().get_object()
        except:
            raise NotFound(
                "Either the team does not exist or you do not have permission to update it.")

        if team.captain != self.request.user:
            raise PermissionDenied(
                "Only the team captain can update this team.")

        return team

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "Team successfully updated",
            "data": response.data
        }, status=status.HTTP_200_OK)


# JOIN AND LEAVE A TEAM AS A PLAYER
class createTeamMember(generics.CreateAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamMember.objects.select_related("user", "team").all()

    def perform_create(self, serializer):
        if TeamMember.objects.filter(user=self.request.user).exists():
            raise PermissionDenied("You are already in a team.")

        team_id = self.kwargs.get("team_id")
        try:
            team = Teams.objects.get(id=team_id)
        except:
            raise NotFound("Team does not exist.")
        serializer.save(user=self.request.user, team=team, role="player")


class leaveTeam(generics.DestroyAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return TeamMember.objects.filter(role="player")

    def get_object(self):
        try:
            team_member = TeamMember.objects.get(user=self.request.user)
        except TeamMember.DoesNotExist:
            raise NotFound("You are not part of any team.")

        if team_member.role == "captain":
            raise PermissionDenied("Captain cannot leave a team.")
        return team_member

    def delete(self, request, *args, **kwargs):
        member = self.get_object()
        response = super().delete(request, *args, **kwargs)
        return Response({"message": "You have successfully left the team."}, status=status.HTTP_200_OK)
