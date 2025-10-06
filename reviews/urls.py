# In reviews/urls.py

from django.urls import path
from .views import ReviewListView, CreateReviewView

urlpatterns = [
    # URL to list reviews for a specific apartment
    # e.g., GET /api/apartments/1/reviews/
    path('apartments/<int:apartment_pk>/reviews/', ReviewListView.as_view(), name='apartment-review-list'),

    # URL to create a new review
    # e.g., POST /api/reviews/create/
    path('reviews/create/', CreateReviewView.as_view(), name='review-create'),
]