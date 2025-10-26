# In bookings/serializers.py

from rest_framework import serializers
from .models import Booking
# --- CHANGE 1: Import the correct serializer ---
from apartments.serializers import UnitSerializer
from core.serializers import UserSerializer
from apartments.models import Unit
import datetime

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing booking details. Includes nested unit and user data.
    """
    # --- CHANGE 2: Use UnitSerializer ---
    unit = UnitSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'unit', 'user', 'check_in', 'check_out', 
            'guests', 'status', 'total_price', 'created_at'
        ]


class CreateBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new booking. Validates input and calculates price.
    """
    # --- CHANGE 3: The primary key now refers to a Unit ---
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.filter(is_active=True), 
        source='unit', 
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['unit_id', 'check_in', 'check_out', 'guests']

    def validate(self, data):
        """
        Perform custom validation for the booking against the UNIT.
        """
        # --- CHANGE 4: The entire validation logic now uses 'unit' ---
        unit = data['unit']
        check_in = data['check_in']
        check_out = data['check_out']

        if check_out <= check_in:
            raise serializers.ValidationError("Check-out date must be after check-in date.")

        overlapping_bookings = Booking.objects.filter(
            unit=unit,
            status__in=['pending', 'confirmed'],
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()

        if overlapping_bookings:
            raise serializers.ValidationError(
                "This unit is already booked for the selected dates."
            )
        
        if data['guests'] > unit.max_guests:
            raise serializers.ValidationError(
                f"The number of guests ({data['guests']}) exceeds the maximum capacity ({unit.max_guests})."
            )

        return data

    def create(self, validated_data):
        # --- CHANGE 5: Price calculation now uses the unit's price ---
        unit = validated_data['unit']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']
        num_nights = (check_out - check_in).days
        total_price = unit.price_per_night * num_nights

        booking = Booking.objects.create(
            user=self.context['request'].user,
            total_price=total_price,
            unit=validated_data.get('unit'),
            check_in=check_in,
            check_out=check_out,
            guests=validated_data.get('guests'),
        )
        return booking
class BookingSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status'] # Only allow updating the status field