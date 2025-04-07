from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
import requests  # для отправки на фандомат

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
                'phone': user.phone
            }
            # отправляем в фандомат
            requests.post(FANDOMAT_URL, json=data)
            return Response({"message": f"Пользователь {user.full_name} успешно отправлен"})
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=404)