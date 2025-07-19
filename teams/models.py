from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# Create your models here.


class Teams(models.Model):
    team_name = models.CharField(
        _("team name"), max_length=50, unique=True, null=False, blank=False)
    team_logo = models.ImageField(
        null=True, blank=True, upload_to="images/", default='images/fallback.png')
    about = models.TextField(
        _('about'), max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    captain = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="team", null=True, blank=True)


class TeamMember(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name="members")
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, null=True, blank=True)
