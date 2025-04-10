from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
import requests  # для отправки на фандомат
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SessionAuth, User
from .serializers import SessionAuthSerializer
from rest_framework.decorators import api_view
import uuid
from django.contrib.auth.hashers import make_password

FANDOMAT_URL = 'http://127.0.0.1:8001/api/welcome/'  # фейковый адрес

# User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        full_name = request.data.get("full_name")
        phone = request.data.get("phone")

        if not all([username, password, full_name, phone]):
            return Response({"error": "Все поля обязательны"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Пользователь уже существует"}, status=400)

        user = User.objects.create(
            username=username,
            password=make_password(password),
            full_name=full_name,
            phone=phone
        )
        return Response({"message": "Пользователь создан", "user_id": user.id}, status=201)
    
class QRScanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qr = request.data.get('qr_code')
        try:
            user = User.objects.get(qr_code=qr)
            data = {
                'username': user.username,
                'full_name': user.full_name,
                'phone': user.phone,
                'balance' : user.balance,
            }
            # отправляем в фандомат
            requests.post(FANDOMAT_URL, json=data)
            return Response({"message": f"Пользователь {user.full_name} успешно отправлен"})
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=404)

# @login_required
def scanner_view(request):
    return render(request, 'scanner.html')

class AuthorizeSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_id = request.data.get("session_id")
        user = request.user

        if not session_id:
            return Response({"detail": "session_id обязателен"}, status=400)

        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            return Response({"detail": "Неверный формат session_id"}, status=400)

        # Сохраняем в базу
        session, created = SessionAuth.objects.update_or_create(
            session_id=session_uuid,
            defaults={"user": user}
        )

        return Response({
            "status": "authorized",
            "session_id": str(session.session_id),
            "user_id": user.id,
            "created": created
        }, status=200)
        
        
@api_view(['GET'])
def session_status(request, session_id):
    try:
        session = SessionAuth.objects.select_related("user").get(session_id=session_id)
        user = session.user
        return Response({
            "authorized": True,
            "user_id": user.id,
            "full_name": user.full_name
        })
    except SessionAuth.DoesNotExist:
        return Response({"authorized": False})

# views.py
from django.views import View
from django.shortcuts import render
from .models import SessionAuth
from django.contrib.auth import get_user_model

User = get_user_model()

class ScannerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        try:
            session_uuid = uuid.UUID(session_id)
            user = request.user  # ← вот тут получаем из токена

            SessionAuth.objects.update_or_create(
                session_id=session_uuid,
                defaults={"user": user}
            )

            return Response({
                "status": "authorized",
                "user_id": user.id,
                "session_id": str(session_uuid)
            })
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class CheckSessionStatusView(APIView):
    def get(self, request, session_id):
        try:
            session = SessionAuth.objects.get(session_id=session_id)
            return Response({
                "authorized": True,
                "user_id": session.user.id,
                "full_name": session.user.full_name
            })
        except SessionAuth.DoesNotExist:
            return Response({"authorized": False})
