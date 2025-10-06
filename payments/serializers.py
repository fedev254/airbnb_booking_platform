# In payments/serializers.py

from rest_framework import serializers
from .models import Payment, Booking
from bookings.serializers import BookingSerializer

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing Payment details.
    """
    booking = BookingSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'provider', 'amount', 'status', 'provider_reference', 'created_at']


class InitiatePaymentSerializer(serializers.Serializer):
    """
    Serializer to receive the booking ID and initiate payment.
    This is not a ModelSerializer because it's for taking action, not creating an object directly from input.
    """
    booking_id = serializers.IntegerField()
    provider = serializers.ChoiceField(choices=Payment.PROVIDER_CHOICES, default=Payment.PROVIDER_CHOICES[0][0]) # Defaults to 'mpesa'

    def validate_booking_id(self, value):
        """
        Check that the booking exists and belongs to the current user and is pending.
        """
        request = self.context.get('request')
        try:
            booking = Booking.objects.get(id=value, user=request.user)
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Booking not found or you do not have permission to pay for it.")

        # Check if the booking is in a state that allows payment
        if booking.status != Booking.STATUS_PENDING:
            raise serializers.ValidationError("This booking is not pending and cannot be paid for.")
        
        return value

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import InitiatePaymentSerializer, PaymentSerializer
from .models import Payment
from bookings.models import Booking

class InitiatePaymentView(generics.GenericAPIView):
    """
    API endpoint to initiate a payment for a booking.
    """
    serializer_class = InitiatePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        booking_id = serializer.validated_data['booking_id']
        booking = Booking.objects.get(id=booking_id)

        # 1. Create a Payment record
        payment = Payment.objects.create(
            booking=booking,
            provider=serializer.validated_data['provider'],
            amount=booking.total_price,
            status='initiated' # Start with 'initiated' status
        )

        # --- 2. (SIMULATION) Call external payment gateway ---
        # In a real application, you would call M-Pesa/Stripe here.
        # For our MVP, we will simulate an immediate successful payment.
        
        # 3. Update status based on payment gateway response
        payment.status = 'success'
        payment.provider_reference = f'SIMULATED__{payment.id}' # Fake reference ID
        payment.save()

        # 4. Update the booking status
        booking.status = Booking.STATUS_CONFIRMED
        booking.save()
        
        # 5. Return the created payment details
        response_serializer = PaymentSerializer(payment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)