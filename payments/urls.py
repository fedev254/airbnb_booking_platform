# In payments/urls.py

from django.urls import path
from .views import InitiatePaymentView

urlpatterns = [
    # The URL to trigger the payment process for a booking
    path('payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
]