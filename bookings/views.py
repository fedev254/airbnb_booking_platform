# In bookings/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, CreateBookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling user bookings.
    - `list`: Returns bookings made by the current authenticated user.
    - `create`: Creates a new booking for the user.
    - `retrieve`: Returns details of a specific booking owned by the user.
    """
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can manage bookings

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
        return self.request.user.bookings.all().order_by('-created_at')

    def perform_create(self, serializer):
        """
        Pass the current user to the serializer's create method.
        (Our serializer now handles this in its context, so this is an alternative way)
        """
        serializer.save() # User is already being added in the serializer's context