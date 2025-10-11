# In core/urls.py

from django.urls import path
from .views import RegisterView, MyTokenObtainPairView
# You'll also need token views for login later
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]