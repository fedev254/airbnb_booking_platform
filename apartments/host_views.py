# In apartments/host_views.py

from rest_framework import viewsets, permissions, generics, exceptions
from .models import Property, BlockedDate, Unit, UnitImage 
from bookings.models import Booking
from .serializers import ( 
    PropertyDetailSerializer, 
    BlockedDateSerializer, 
    UnitImageUploadSerializer
)
from bookings.serializers import BookingSerializer
from core.permissions import IsHostUser
from rest_framework.decorators import action
from rest_framework.response import Response


class HostDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoints for the Host Dashboard.
    Provides views for a host to see their own properties and bookings.
    """
    serializer_class = PropertyDetailSerializer
    permission_classes = [IsHostUser]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user).prefetch_related('units__bookings')

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        host_properties = self.get_queryset()
        bookings = Booking.objects.filter(
            unit__property__in=host_properties
        ).order_by('-created_at')
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class BlockedDateViewSet(viewsets.ModelViewSet):
    """
    Endpoint for hosts to manage blocked dates for their units.
    """
    serializer_class = BlockedDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BlockedDate.objects.filter(unit__property__owner=self.request.user)


class UnitImageUploadView(generics.CreateAPIView):
    """
    API endpoint for a host to upload an image for a unit they own.
    """
    queryset = UnitImage.objects.all()
    serializer_class = UnitImageUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        unit_pk = self.kwargs.get('unit_pk')
        try:
            unit = Unit.objects.get(pk=unit_pk)
        except Unit.DoesNotExist:
            # --- CHANGE 1: Use exceptions from rest_framework ---
            raise exceptions.NotFound("Unit not found.")

        if unit.property.owner != self.request.user:
            # --- CHANGE 2: Use exceptions from rest_framework ---
            raise exceptions.PermissionDenied(
                "You do not have permission to add images to this unit."
            )
            
        serializer.save(unit=unit)