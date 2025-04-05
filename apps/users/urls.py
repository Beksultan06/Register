from django.urls import path
from .views import UserAPIView , UserRegisterAPI

urlpatterns = [
    path('', UserAPIView.as_view(), name="api users list"),
    path('register/', UserRegisterAPI.as_view(), name="users register api"),
]