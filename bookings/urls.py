# In bookings/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import BookingViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my-bookings'),
]