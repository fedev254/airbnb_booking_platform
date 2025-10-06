# In reviews/serializers.py

from rest_framework import serializers
from .models import Review
from bookings.models import Booking
from core.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying a review. Includes read-only user details.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']


class CreateReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new review for a booking.
    """
    booking_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['booking_id', 'rating', 'comment']

    def validate(self, data):
        booking_id = data['booking_id']
        request = self.context.get('request')
        
        # 1. Check if the booking exists, belongs to the user, and is completed.
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Booking not found or you do not have permission to review it.")
        
        if booking.status != Booking.STATUS_COMPLETED:
            raise serializers.ValidationError("You can only review bookings that have been completed.")

        # 2. Check if a review already exists for this booking/apartment by this user.
        if Review.objects.filter(apartment=booking.apartment, user=request.user).exists():
            raise serializers.ValidationError("You have already submitted a review for this apartment.")
            
        # Add the validated apartment to the data for the create method
        data['apartment'] = booking.apartment
        return data

    def create(self, validated_data):
        # The user is the one making the request.
        # The apartment was added during validation.
        # Pop the extra 'booking_id' field.
        validated_data.pop('booking_id')
        review = Review.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        return review