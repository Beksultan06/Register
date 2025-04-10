from django.urls import path
from .views import RegisterView, QRScanView, scanner_view, AuthorizeSessionView, session_status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('scan/', QRScanView.as_view()),
    path('scanner/', scanner_view, name='scanner'),
    path('api/authorize/', AuthorizeSessionView.as_view(), name='authorize'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('api/session-status/<uuid:session_id>/', session_status),
]
