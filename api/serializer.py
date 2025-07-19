from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from teams.models import Teams


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def get_token(self, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['user_name'] = user.user_name
        # Add custom claims if needed
        return token

    def validate(self, attrs):
        # Override 'username' to 'email'
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ["id", "team_name", 'team_logo', 'captain']


class UserSerializer(serializers.ModelSerializer):
    # author_team_name = serializers.SerializerMethodField()
    team = TeamSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "user_name", "first_name", 'password',
                  "about", "profilePic", 'team']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
