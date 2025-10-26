# airbnb_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# For Google Login Integration
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    # ----------------------------
    # ⚙️ Admin Panel
    # ----------------------------
    path('admin/', admin.site.urls),

    # ----------------------------
    # 🔐 Authentication Endpoints
    # ----------------------------
    # Custom core auth (register, login/token, profile, etc.)
    path('api/auth/', include('core.urls')),

    # dj-rest-auth endpoints (password reset, logout, etc.)
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # ✅ Correct Google login endpoint
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),

    # ✅ Required for social logins (safe to include)
    path('accounts/', include('allauth.urls')),

    # ----------------------------
    # 🏡 Host-specific Routes
    # ----------------------------
    path('api/host/', include('apartments.host_urls')),

    # ----------------------------
    # 🌍 Public / Customer Routes
    # ----------------------------
    path('api/', include('apartments.urls')),
    path('api/', include('bookings.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('reviews.urls')),

    # ----------------------------
    # ⚙️ Default Django Auth (optional)
    # ----------------------------
    path('auth/', include('django.contrib.auth.urls')),

    path('sentry-debug/', trigger_error),
    path('api/blog/', include('blog.urls')),
]

# ✅ Serve media during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
