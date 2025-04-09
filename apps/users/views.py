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

FANDOMAT_URL = 'http://127.0.0.1:8001/api/welcome/'  # фейковый адрес

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []

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

@login_required
def scanner_view(request):
    return render(request, 'scanner.html')

class AuthorizeSessionView(APIView):
    def post(self, request):
        session_id = request.data.get('session_id')
        user_id = request.data.get('user_id')

        if not session_id or not user_id:
            return Response({"detail": "session_id и user_id обязательны"}, status=400)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=404)

        session_obj, created = SessionAuth.objects.update_or_create(
            session_id=uuid.UUID(session_id),
            defaults={"user": user}
        )
        return Response({"status": "ok"}, status=200)


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

class ScannerRedirectView(View):
    def get(self, request, session_id):
        try:
            # ⚠️ Вместо этого — в будущем авторизованный пользователь из мобильного приложения
            user = User.objects.get(id=1)  # для теста

            SessionAuth.objects.update_or_create(
                session_id=session_id,
                defaults={"user": user}
            )
            return render(request, "scanner_success.html", {"user": user})
        except Exception as e:
            return render(request, "scanner_fail.html", {"error": str(e)})

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
