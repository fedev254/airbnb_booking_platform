# In payments/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import InitiatePaymentSerializer, PaymentSerializer
from .models import Payment
from bookings.models import Booking

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class InitiatePaymentView(generics.GenericAPIView): # <--- CHECK THIS LINE CAREFULLY
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

        try:
            subject = f"Your Booking Confirmation for {booking.apartment.title}"
            context = {'booking': booking, 'user': request.user}
            html_message = render_to_string('emails/booking_confirmation.html', context)
            plain_message = "Your booking is confirmed. Please see the attached HTML for details." # Fallback
            from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@example.com'
            recipient_list = [request.user.email]

            send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        except Exception as e:
            # In a real app, you'd log this error
            print(f"Error sending email: {e}")
        
        # 5. Return the created payment details
        response_serializer = PaymentSerializer(payment)
        return Response(response_serializer.data, status=status.HTTP_2_CREATED)