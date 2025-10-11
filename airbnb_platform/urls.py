# In airbnb_platform/urls.py

from django.contrib import admin
from django.urls import path, include
# --- 1. Add these two imports ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Host specific URLs
    path('api/host/', include('apartments.host_urls')),

    # Public & Customer URLs
    path('api/auth/', include('core.urls')), 
    path('api/', include('apartments.urls')), 
    path('api/', include('bookings.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('reviews.urls')), 
]

# --- 2. Add this block at the end of the file ---
# This is crucial for serving user-uploaded media files (like images)
# during development. This will NOT work in production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)