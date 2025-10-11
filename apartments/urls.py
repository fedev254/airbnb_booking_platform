# In apartments/urls.py

from django.urls import path, include
from rest_framework_nested import routers
from .views import PropertyViewSet, UnitViewSet

# Primary router for top-level resources
router = routers.DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'units', UnitViewSet, basename='unit-search') # For general searching

# This allows nested URLs like /api/properties/{property_pk}/units/
properties_router = routers.NestedSimpleRouter(router, r'properties', lookup='property')

# The final URLs are now determined automatically by the routers.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(properties_router.urls)),
]