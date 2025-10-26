# In gunicorn_config.py

# The socket to bind to.
# A path is used for a Unix socket.
# bind = "unix:/run/gunicorn.sock" 

# An IP address and port is used for a TCP socket.
bind = "0.0.0.0:8000"

# The number of worker processes for handling requests.
workers = 3

# The user and group to run as.
# user = "nobody"
# group = "nogroup"

# The WSGI application to run.
wsgi_app = "airbnb_platform.wsgi:application"

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"