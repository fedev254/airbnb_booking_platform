from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, UserProfileSerializer
from .models import User
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse


@method_decorator(ratelimit(key='ip', rate='10/h', method='POST', block=True), name='dispatch')
class RegisterView(generics.CreateAPIView):
    """
    API endpoint for new user registration.
    Accessible by anyone.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


# ✅ Added block=True here
@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
class MyTokenObtainPairView(TokenObtainPairView):
    """
    Takes a user's username and password and returns JWT token.
    NOW RATE-LIMITED to 5 attempts per minute from the same IP.
    """
    serializer_class = MyTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:5173"
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        print("📩 Incoming Google login data:", request.data)
        print("📩 Request headers:", dict(request.headers))
        
        try:
            response = super().post(request, *args, **kwargs)
            print("✅ Google login success — status:", response.status_code)
            print("✅ Response data:", response.data)
            return response
        except Exception as e:
            import traceback
            import sys
            from rest_framework.response import Response
            from rest_framework import status

            print("❌ Google login backend exception:", str(e))
            print("❌ Exception type:", type(e).__name__)
            traceback.print_exc()

            if hasattr(e, "response") and hasattr(e.response, "text"):
                print("📜 Google error response:", e.response.text)

            return Response(
                {"error": str(e), "type": type(e).__name__}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
def custom_ratelimit_handler(request, exception=None):
    """
    Custom handler for rate-limited requests.
    Returns a clean 429 response instead of a 500.
    """
    return JsonResponse(
        {
            "detail": "Too many login attempts. Please try again later.",
            "status_code": 429
        },
        status=429
    )
