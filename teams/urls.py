from django.urls import path
from . import views

urlpatterns = [
    path("teams/", views.CreateAndGetTeams.as_view(), name="get-teams"),
    path("teams/delete/<int:pk>/", views.deleteTeam.as_view(), name="delete-team"),
    path("teams/<int:pk>/", views.getOneTeam.as_view(), name="get-one-team"),
    path("teams/<int:pk>/update/", views.updateTeam.as_view(), name="update-team"),
    path("teams/join/<int:team_id>/",
         views.createTeamMember.as_view(), name="join-team"),
    path("teams/leave/", views.leaveTeam.as_view(), name="leave-team")
]
