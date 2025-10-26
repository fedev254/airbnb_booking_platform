# core/urls.py
from django.urls import path, include
from .views import RegisterView, MyTokenObtainPairView, UserProfileView, GoogleLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserProfileView.as_view(), name='user-profile'),

    # ✅ Password Reset endpoints (dj-rest-auth)
    path('password/reset/', include('dj_rest_auth.urls')),  # includes password_reset and confirm
    path('google/', GoogleLoginView.as_view(), name='google_login'),


]
