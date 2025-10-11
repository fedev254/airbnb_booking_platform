# In core/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    """
    API endpoint for new user registration.
    Accessible by anyone.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny] # Anyone can register
    serializer_class = RegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer