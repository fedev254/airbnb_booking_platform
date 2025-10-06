# In reviews/views.py

from rest_framework import generics, permissions
from .models import Review, Apartment
from .serializers import ReviewSerializer, CreateReviewSerializer

class ReviewListView(generics.ListAPIView):
    """
    API endpoint to list all reviews for a specific apartment.
    Accessible by anyone.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny] # Anyone can view reviews

    def get_queryset(self):
        """
        Filter reviews by the apartment ID provided in the URL.
        """
        apartment_id = self.kwargs['apartment_pk']
        return Review.objects.filter(apartment_id=apartment_id).order_by('-created_at')


class CreateReviewView(generics.CreateAPIView):
    """
    API endpoint for an authenticated user to create a new review.
    """
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer
    permission_classes = [permissions.IsAuthenticated] # Must be logged in to create a review