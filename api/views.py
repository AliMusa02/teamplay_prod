from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializer import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "User created successfully!",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": "User creation failed.",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GetUser(generics.RetrieveAPIView):
    queryset = User.objects.select_related('team').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "message": "User fetched successfully!",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Failed to fetch user.",
                "details": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
