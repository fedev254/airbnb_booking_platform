# In apartments/host_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .host_views import HostDashboardViewSet, BlockedDateViewSet, HostUnitImageViewSet, ReviewViewSet, UnitImageUploadView, HostUnitViewSet, HostBookingManageViewSet, HostAnalyticsView

router = DefaultRouter()
router.register(r'dashboard', HostDashboardViewSet, basename='host-dashboard')
router.register(r'blocked-dates', BlockedDateViewSet, basename='host-blocked-dates')
router.register(r'units', HostUnitViewSet, basename='host-units')
router.register(r'unit-images', HostUnitImageViewSet, basename='host-unit-images')
router.register(r'manage-bookings', HostBookingManageViewSet, basename='host-manage-bookings')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('units/<int:unit_pk>/add-image/', UnitImageUploadView.as_view(), name='unit-add-image'),
    path('analytics/', HostAnalyticsView.as_view(), name='host-analytics'),
]