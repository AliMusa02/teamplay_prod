from rest_framework import serializers
from .models import Teams, TeamMember
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_name", "first_name", "profilePic"]


class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeamMember
        fields = ["id", "user", "role", "joined_at"]


class TeamSerializer(serializers.ModelSerializer):
    # captain = UserSerializer(read_only=True)
    captain_id = serializers.IntegerField(
        source='captain.id', read_only=True)
    captain_username = serializers.CharField(
        source='captain.user_name', read_only=True)
    members = serializers.SerializerMethodField()

    def get_captain_id(self, obj):
        return obj.captain.id if obj.captain else None

    def get_captain_username(self, obj):
        return obj.captain.user_name if obj.captain else None

    class Meta:
        model = Teams
        fields = ["id", "team_name", "team_logo",
                  "about", "created_at", "captain_id", "captain_username", "members"]

    def get_members(self, obj):
        team_members = obj.members.select_related("user").order_by('joined_at')
        return TeamMemberSerializer(team_members, many=True).data
