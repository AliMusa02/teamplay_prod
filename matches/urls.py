from django.urls import path
from . import views

urlpatterns = [
    path("invitations/get-post/", views.CreateAndGetInvitations.as_view(),
         name="get-create-invitations"),
    path("invitations/update/<int:id>/",
         views.UpdateInvitation.as_view(), name="update-status"),
    path("invitations/get-all/", views.GetAllinvitations.as_view(), name="get-all"),
    path("matches/all/", views.GetAllMatches.as_view(), name="matches-all"),
    path("matches/<int:team_id>/",
         views.GetOwnMatches.as_view(), name="get-own-matches")

]
