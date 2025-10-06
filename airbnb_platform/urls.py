# In airbnb_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # API URLs
    path('api/auth/', include('core.urls')), # For registration and login
    path('api/', include('apartments.urls')),
    path('api/', include('bookings.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('reviews.urls')),
    # You will add other app urls here later
    # path('api/', include('bookings.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)