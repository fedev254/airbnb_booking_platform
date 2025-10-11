# In reviews/views.py

from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer, CreateReviewSerializer

class ReviewListView(generics.ListAPIView):
    """
    API endpoint to list all reviews for a specific Property.
    Accessible by anyone.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Filter reviews by the property ID (property_pk) provided in the URL.
        """
        property_pk = self.kwargs['property_pk']
        return Review.objects.filter(property_id=property_pk).order_by('-created_at')


class CreateReviewView(generics.CreateAPIView):
    """
    API endpoint for an authenticated user to create a new review.
    """
    serializer_class = CreateReviewSerializer
    permission_classes = [permissions.IsAuthenticated]