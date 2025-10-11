# In apartments/host_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .host_views import HostDashboardViewSet, BlockedDateViewSet, UnitImageUploadView

router = DefaultRouter()
router.register(r'dashboard', HostDashboardViewSet, basename='host-dashboard')
router.register(r'blocked-dates', BlockedDateViewSet, basename='host-blocked-dates')

urlpatterns = [
    path('', include(router.urls)),
    path('units/<int:unit_pk>/add-image/', UnitImageUploadView.as_view(), name='unit-add-image'),
    
]