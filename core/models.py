# airbnb_backend_project/core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# --- 1. Custom User Model ---
# This is the single source of truth for the User.
# It's best practice to keep this in a central 'core' or 'users' app.
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    This model is the single source of truth for user accounts.
    """
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        HOST = 'HOST', 'Host'
        ADMIN = 'ADMIN', 'Admin'

    # The email field is inherited from AbstractUser and is used for login.
    # The username field is also inherited but we will primarily use email.

    # Adding fields as per project documentation
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    # Optional: Add other fields if needed in the future
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        # Using email for string representation is often more useful in APIs.
        return self.email