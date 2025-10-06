# In apartments/views.py

from rest_framework import viewsets, permissions
from .models import Apartment
from .serializers import ApartmentSerializer

class ApartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows apartments to be viewed or edited.
    - List all active apartments.
    - Create a new apartment (must be authenticated).
    - Retrieve, update, or delete a specific apartment.
    """
    queryset = Apartment.objects.filter(is_active=True).prefetch_related('images')
    serializer_class = ApartmentSerializer
    
    # Permissions: Anyone can view, but only authenticated users can create/edit.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]