from rest_framework import serializers
from .models import Posts
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(
        source='author.id', read_only=True)
    author_username = serializers.CharField(
        source='author.user_name', read_only=True)
    author_profilePic = serializers.ImageField(
        source='author.profilePic', read_only=True)
    # author_team_name = serializers.CharField(
    #     source='author.team.team_name', null=True, blank=True, read_only=True)
    author_team_name = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ["id", "content", "created_at", "post_pic", "author_id",
                  'author_username', 'author_profilePic', 'author_team_name']
        # extra_kwargs = {"author_username": {"read_only": True}, "author_profilePic": {
        #     "read_only": True}, "author_team_name": {"read_only": True}}

    def get_author_team_name(self, obj):
        try:
            return obj.author.team.team_name
        except AttributeError:
            return "User has no team"
        # except Exception:
        #     return None
