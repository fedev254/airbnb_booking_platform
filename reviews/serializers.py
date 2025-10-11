# In reviews/serializers.py

from rest_framework import serializers
from .models import Review
from bookings.models import Booking
from core.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'property', 'unit', 'rating', 'comment', 'created_at']


class CreateReviewSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['booking_id', 'rating', 'comment']

    def validate(self, data):
        booking_id = data['booking_id']
        request = self.context.get('request')
        
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Booking not found or you do not have permission to review it.")
        
        if booking.status != Booking.STATUS_COMPLETED:
            raise serializers.ValidationError("You can only review bookings that have been completed.")

        if Review.objects.filter(property=booking.unit.property, user=request.user).exists():
            raise serializers.ValidationError("You have already submitted a review for this property.")
            
        # Add validated property and unit to the data
        data['property'] = booking.unit.property
        data['unit'] = booking.unit
        return data

    def create(self, validated_data):
        validated_data.pop('booking_id')
        review = Review.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        return review