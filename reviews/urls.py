# In reviews/urls.py

from django.urls import path
from .views import ReviewListView, CreateReviewView

urlpatterns = [
    # URL to list reviews for a specific property
    # e.g., GET /api/properties/1/reviews/
    path('properties/<int:property_pk>/reviews/', ReviewListView.as_view(), name='property-review-list'),

    # URL to create a new review
    # e.g., POST /api/reviews/create/
    path('reviews/create/', CreateReviewView.as_view(), name='review-create'),
]