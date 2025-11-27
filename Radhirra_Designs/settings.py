"""
Django settings for Radhirra_Designs project.
"""

from pathlib import Path
import os
import dj_database_url
import cloudinary
import cloudinary_storage
import mimetypes
from dotenv import load_dotenv

load_dotenv()

mimetypes.add_type("text/css", ".css", True)

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# SECURITY SETTINGS
# -----------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-7agyh2+egfz%l^o+-4=ht$ixcw*bdhx^hq)ogy-=qrk++)dpgq",
)

DEBUG = os.environ.get("RENDER", "") != "true"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = (
    [f"https://{RENDER_EXTERNAL_HOSTNAME}"] if RENDER_EXTERNAL_HOSTNAME else []
)


# -----------------------------
# INSTALLED APPS
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Your apps
    "Radhirra",
    "users",
    # Cloudinary
    "cloudinary",
    "cloudinary_storage",
    # Forms
    "crispy_forms",
    "crispy_bootstrap5",
]


# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# -----------------------------
# TEMPLATES
# -----------------------------
ROOT_URLCONF = "Radhirra_Designs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Radhirra_Designs.wsgi.application"


# -----------------------------
# DATABASE (RENDER POSTGRES)
# -----------------------------
DATABASES = {
    "default": dj_database_url.parse(
        "postgresql://rameshwari:do4tuozi4MD7Drvv9LWa2aSazM17zPke@dpg-d4i573umcj7s73cd7nu0-a.oregon-postgres.render.com/radhirra",
        conn_max_age=600,
        ssl_require=True,
    )
}


# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -----------------------------
# STATIC & MEDIA FILES
# -----------------------------

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -----------------------------
# CLOUDINARY CONFIG
# -----------------------------
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")

# Initialize Cloudinary (IMPORTANT)
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
    "API_KEY": CLOUDINARY_API_KEY,
    "API_SECRET": CLOUDINARY_API_SECRET,
}


# -----------------------------
# AUTH MODEL
# -----------------------------
AUTH_USER_MODEL = "users.CustomUser"


# -----------------------------
# CRISPY FORMS
# -----------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# -----------------------------
# DEFAULT PK
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
