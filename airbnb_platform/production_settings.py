# In airbnb_platform/production_settings.py

from .settings import * # Import all base settings

# --- PRODUCTION-SPECIFIC OVERRIDES ---

DEBUG = False # CRITICAL: Never run with DEBUG=True in production

# Configure ALLOWED_HOSTS with your future domain name
ALLOWED_HOSTS = [
    'your-api-domain.com', # e.g., 'api.stayease.com'
    # You'll get this from your hosting provider (like Render)
    'your-app-name.onrender.com', 
]

# Use whitenoise to serve static files efficiently
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'