# In apartments/views.py

from rest_framework import viewsets, permissions
from .models import Property, Unit
from rest_framework.views import APIView
from .serializers import PropertySerializer, UnitSerializer, PropertyDetailSerializer
from .filters import UnitFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsHostOrAdminOrReadOnly

class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing Properties (Buildings/Complexes).
    - List view uses a simpler serializer.
    - Detail view uses a serializer with nested units.
    """
    queryset = Property.objects.all()
    permission_classes = [IsHostOrAdminOrReadOnly]
    
    serializer_class = PropertyDetailSerializer
    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user as the owner of the new property.
        """
        serializer.save(owner=self.request.user)

class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for searching and viewing individual Units.
    This is the main endpoint for a customer looking for a place to book.
    It is ReadOnly because Units are managed through their parent Property.
    """
    queryset = Unit.objects.filter(is_active=True, property__is_active=True).select_related('property')
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny] # Anyone can search for units
    filterset_class = UnitFilter

class HostDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Return only properties owned by the logged-in host
        properties = Property.objects.filter(owner=request.user).prefetch_related('units__images')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)