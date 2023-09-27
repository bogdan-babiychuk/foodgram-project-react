from django.shortcuts import render
from .serializers import UserCreateSerializer, UserSerializer
from .models import User
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
