from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView

from .models import User
from .serializers import UserSerializer, UserRegisterSerializer

# Create your views here.
class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer