# In bookings/serializers.py

from rest_framework import serializers
from .models import Booking
from apartments.serializers import ApartmentSerializer
from core.serializers import UserSerializer
from apartments.models import Apartment
import datetime

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing booking details. Includes nested apartment and user data.
    """
    apartment = ApartmentSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'apartment', 'user', 'check_in', 'check_out', 
            'guests', 'status', 'total_price', 'created_at'
        ]


class CreateBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new booking. Validates input and calculates price.
    """
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartment.objects.filter(is_active=True), 
        source='apartment', 
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['apartment_id', 'check_in', 'check_out', 'guests']

    def validate(self, data):
        """
        Perform custom validation for the booking.
        """
        # 1. Check that check_out date is after check_in date
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")

        # 2. Check that the apartment is not already booked for the selected dates
        apartment = data['apartment']
        check_in = data['check_in']
        check_out = data['check_out']
        
        overlapping_bookings = Booking.objects.filter(
            apartment=apartment,
            status__in=['pending', 'confirmed'],
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()

        if overlapping_bookings:
            raise serializers.ValidationError(
                "This apartment is already booked for the selected dates."
            )
        
        # 3. Check if the number of guests does not exceed the apartment's capacity
        if data['guests'] > apartment.max_guests:
            raise serializers.ValidationError(
                f"The number of guests ({data['guests']}) exceeds the maximum capacity ({apartment.max_guests})."
            )

        return data

    def create(self, validated_data):
        """
        Create the booking instance, assign the user, and calculate the total price.
        """
        apartment = validated_data['apartment']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']

        # Calculate number of nights
        num_nights = (check_out - check_in).days
        if num_nights <= 0:
            num_nights = 1 # Minimum 1 night charge

        # Calculate total price
        total_price = apartment.price_per_night * num_nights

        # Create the booking instance
        booking = Booking.objects.create(
            user=self.context['request'].user,
            total_price=total_price,
            **validated_data
        )
        return booking