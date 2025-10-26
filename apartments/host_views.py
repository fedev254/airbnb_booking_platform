# In apartments/host_views.py

from rest_framework import viewsets, permissions, generics, exceptions, status
from .models import Property, BlockedDate, Unit, UnitImage 
from bookings.models import Booking
from .serializers import ( 
    PropertyDetailSerializer, 
    BlockedDateSerializer,
    UnitImageSerializer, 
    UnitImageUploadSerializer,
    UnitSerializer
)
from django.db.models.functions import TruncMonth

from django.db.models import Sum, Avg, Count
from bookings.serializers import BookingSerializer, BookingStatusUpdateSerializer
from core.permissions import IsHostUser
from rest_framework.decorators import action
from rest_framework.response import Response
from reviews.models import Review         # 👈 1. Import Review
from reviews.serializers import ReviewSerializer # 👈 2. Import ReviewSerializer
from rest_framework.views import APIView
from datetime import datetime

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
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """
        Custom action to retrieve all reviews for properties
        owned by the current host.
        """
        host_properties = Property.objects.filter(owner=request.user)
        reviews = Review.objects.filter(property__in=host_properties).order_by('-created_at')

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ReviewSerializer(reviews, many=True)
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
class HostUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for hosts to perform CRUD operations on their own units.
    """
    serializer_class = UnitSerializer # We can reuse our existing serializer
    permission_classes = [IsHostUser]

    def get_queryset(self):
        """Ensure hosts can only manage units belonging to their properties."""
        return Unit.objects.filter(property__owner=self.request.user)
        
    def perform_create(self, serializer):
        """Ensure the new unit is associated with one of the host's properties."""
        # This will require the frontend to send the property_id
        # We can add validation for that here.
        property_id = self.request.data.get('property')
        prop = Property.objects.get(pk=property_id)
        if prop.owner != self.request.user:
            raise PermissionDenied("You do not own this property.")
        serializer.save()
class HostUnitImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for a host to manage images for their own units.
    Supports deleting (destroy) and updating (caption).
    """
    serializer_class = UnitImageSerializer
    permission_classes = [IsHostUser]

    def get_queryset(self):
        """Ensures a host can only manage images belonging to their own units."""
        return UnitImage.objects.filter(unit__property__owner=self.request.user) 

class HostBookingManageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for hosts to manage (view, update, cancel) bookings for their own properties.
    """
    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [IsHostUser]

    def get_queryset(self):
        """Ensures a host can only manage bookings for their own properties."""
        return Booking.objects.filter(unit__property__owner=self.request.user)   
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=True, methods=['patch'], url_path='mark_as_read')
    def mark_as_read(self, request, pk=None):
        review = self.get_object()
        review.read = True
        review.save()
        return Response({"message": "Review marked as read"}, status=status.HTTP_200_OK)
    

class HostAnalyticsView(APIView):
    permission_classes = [IsHostUser]

    def get(self, request, *args, **kwargs):
        # Get all confirmed bookings for properties owned by this host
        confirmed_bookings = Booking.objects.filter(
            unit__property__owner=request.user,
            status='confirmed'
        )

        # 1. Total Revenue
        total_revenue = confirmed_bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0

        # 2. Active (Upcoming) Bookings Count
        active_bookings_count = confirmed_bookings.filter(check_out__gte=datetime.today()).count()

        # 3. Total Nights Booked
        total_nights = sum([(b.check_out - b.check_in).days for b in confirmed_bookings])
        monthly_revenue = confirmed_bookings.annotate(
            month=TruncMonth('check_in') # Truncate the check_in date to the 1st of its month
        ).values('month').annotate(
            total=Sum('total_price') # Sum all prices for that month
        ).order_by('month')
        # 4. Average Guest Rating
        avg_rating_query = Review.objects.filter(property__owner=request.user).aggregate(Avg('rating'))
        average_rating = avg_rating_query['rating__avg'] or 0
        chart_labels = [m['month'].strftime('%b %Y') for m in monthly_revenue]
        chart_data = [m['total'] for m in monthly_revenue]
        # Assemble the data
        data = {
            'total_properties': Property.objects.filter(owner=request.user).count(),
            'total_revenue': total_revenue,
            'active_bookings_count': active_bookings_count,
            'total_nights_booked': total_nights,
            'average_rating': round(average_rating, 2),
            'monthly_revenue_chart': {
                'labels': chart_labels,
                'data': chart_data
            }
            # We can add monthly revenue data for charts here later
        }

        return Response(data)