from django.urls import path
from .views import RegisterView, QRScanView, scanner_view, AuthorizeSessionView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from .views import session_status


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),  # JWT login
    path('token/refresh/', TokenRefreshView.as_view()),
    path('scan/', QRScanView.as_view()),
    path('scanner/', scanner_view, name='scanner'),
    path('api/authorize/', AuthorizeSessionView.as_view()),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('api/session-status/<uuid:session_id>/', session_status),

]

