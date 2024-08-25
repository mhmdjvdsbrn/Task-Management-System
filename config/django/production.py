from .base import *  # noqa
from decouple import config, Csv


APP_DOMAIN = config("APP_DOMAIN", default="http://localhost:8000")

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

CORS_ALLOW_ALL_ORIGINS = False

#config later for used .env
# CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS').split(',')
CORS_ALLOWED_ORIGINS = [
    # Add the origin(s) of your React app here
    "http://localhost:5173",
    "http://localhost:3000",
    # "https://your-react-app-domain.com",  # Example: for production
]

CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', default=[],cast=Csv())
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)


# Use the secure proxy header to detect the protocol when behind a proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)

# Prevent content type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = config("SECURE_CONTENT_TYPE_NOSNIFF", default=True)

