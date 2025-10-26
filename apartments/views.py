# In apartments/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from .models import Property, PropertyImage, Unit, UnitImage
from .serializers import (
    PropertySerializer, 
    PropertyImageSerializer,  # 👈 Make sure this import exists
    PropertyDetailSerializer,
    UnitSerializer, 
    UnitImageSerializer
)
from .filters import UnitFilter, PropertyFilter
from core.permissions import IsHostOrAdminOrReadOnly
from datetime import date, timedelta

class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing Properties (Buildings/Complexes).
    """
    queryset = Property.objects.all()
    permission_classes = [IsHostOrAdminOrReadOnly]
    serializer_class = PropertyDetailSerializer
    filterset_class = PropertyFilter
    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user as the owner of the new property.
        """
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload a new image for a property."""
        property_obj = self.get_object()
        
        # Check if user owns this property
        if property_obj.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to upload images to this property.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PropertyImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property=property_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='delete-image/(?P<image_id>[^/.]+)')
    def delete_image(self, request, pk=None, image_id=None):
        """Delete an existing property image."""
        property_obj = self.get_object()
        
        # Check if user owns this property
        if property_obj.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to delete images from this property.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            image = property_obj.images.get(id=image_id)
            image.delete()
            return Response(
                {'detail': 'Image deleted successfully'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except PropertyImage.DoesNotExist:
            return Response(
                {'detail': 'Image not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for searching and viewing individual Units.
    """
    queryset = Unit.objects.filter(is_active=True, property__is_active=True).select_related('property')
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = UnitFilter


class HostDashboardView(APIView):
    """
    API endpoint for host dashboard - shows properties owned by the current user.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        properties = Property.objects.filter(owner=request.user).prefetch_related('units__images')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)


class UnitImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing unit images.
    """
    queryset = UnitImage.objects.all()
    serializer_class = UnitImageSerializer
    permission_classes = [IsAuthenticated]


# 👇 ALTERNATIVE: Function-based view (as shown in the instruction)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_property_image(request, property_pk):
    """
    Function-based view to upload property image.
    Use this if you prefer function-based views over ViewSet actions.
    """
    try:
        prop = Property.objects.get(pk=property_pk, owner=request.user)
    except Property.DoesNotExist:
        return Response(
            {'detail': 'Property not found or you do not have permission.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
        
    image_serializer = PropertyImageSerializer(data=request.data)
    if image_serializer.is_valid():
        image_serializer.save(property=prop)
        return Response(image_serializer.data, status=status.HTTP_201_CREATED)
    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny]) # This data is safe to be public
def get_unit_availability(request, unit_id):
    """
    Returns a list of all dates that are booked or blocked for a specific unit.
    """
    try:
        unit = Unit.objects.get(pk=unit_id)
    except Unit.DoesNotExist:
        return Response({'detail': 'Unit not found.'}, status=404)
    
    # Get all confirmed or pending bookings
    booked_dates = []
    bookings = unit.bookings.filter(status__in=['confirmed', 'pending'])
    for booking in bookings:
        # Generate all dates from check-in to (but not including) check-out
        current_date = booking.check_in
        while current_date < booking.check_out:
            booked_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
            
    # Get all host-blocked dates
    blocked_dates = []
    blocks = unit.blocked_dates.all()
    for block in blocks:
        current_date = block.start_date
        while current_date <= block.end_date:
            blocked_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
            
    # Combine and remove duplicates, then return
    all_unavailable_dates = sorted(list(set(booked_dates + blocked_dates)))
    
    return Response(all_unavailable_dates)

