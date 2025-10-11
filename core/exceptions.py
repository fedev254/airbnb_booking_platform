# In core/exceptions.py

from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If it's a 500 Internal Server Error, we customize the response
    if response is not None and response.status_code >= 500:
        # We can create a more generic error message
        custom_data = {
            'detail': 'An internal server error occurred. Please try again later.'
        }
        # Log the original error to the console for debugging
        print(f"--- SERVER CRASH ---")
        print(f"Exception: {str(exc)}")
        print(f"Context: {context}")
        print(f"--- END TRACE ---")
        
        # Re-create the response with our custom data
        response.data = custom_data
        
    elif response is None:
        # If DRF can't handle the exception, we create our own 500 response
        print(f"--- UNHANDLED SERVER CRASH ---")
        print(f"Exception: {str(exc)}")
        print(f"--- END TRACE ---")
        return Response({'detail': f'Unhandled server error: {str(exc)}'}, status=500)

    return response