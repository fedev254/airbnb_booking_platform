# In bookings/views.py
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, CreateBookingSerializer
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling user bookings.
    - `list`: Returns bookings made by the current authenticated user.
    - `create`: Creates a new booking for the user (rate limited to 5 per minute).
    - `retrieve`: Returns details of a specific booking owned by the user.
    """
    
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can manage bookings

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the request action.
        - Use CreateBookingSerializer for the 'create' action.
        - Use BookingSerializer for all other actions ('list', 'retrieve').
        """
        if self.action == 'create':
            return CreateBookingSerializer
        return BookingSerializer

    def get_queryset(self):
        """
        This view should only return bookings for the currently authenticated user.
        """
        return Booking.objects.filter(user=self.request.user).select_related(
            'unit__property'
        ).prefetch_related('unit__images')

    @method_decorator(ratelimit(key='user', rate='5/m', method='POST'), name='create')
    def create(self, request, *args, **kwargs):
        """
        Create a new booking with rate limiting (5 bookings per minute per user).
        """
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Pass the current user to the serializer's create method.
        """
        serializer.save(user=self.request.user)

class MyBookingsView(APIView):
    """
    API endpoint to get all bookings for the current user.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).select_related(
            'unit__property'
        ).prefetch_related('unit__images')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)