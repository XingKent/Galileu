# galileu-backend/src/config/settings/base.py

import os
from pathlib import Path

# ============================================================
# Helpers
# ============================================================

def env(key: str, default=None):
    return os.getenv(key, default)


def env_bool(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "y", "on")


def env_list(key: str, default: str = ""):
    raw = os.getenv(key, default) or ""
    return [x.strip() for x in raw.split(",") if x.strip()]


# ============================================================
# Paths
# Estrutura: src/config/settings/base.py  -> BASE_DIR = src/
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

# ============================================================
# Core
# ============================================================

SECRET_KEY = env("DJANGO_SECRET_KEY", "insecure-change-me")
DEBUG = env_bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,0.0.0.0,web,nginx",
)

# ============================================================
# Apps
# ============================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    # Local
    "apps.accounts",
    "apps.teams",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # precisa ficar no topo
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ============================================================
# Database
# - Se tiver variáveis de Postgres, usa Postgres
# - Senão cai pra SQLite
# ============================================================

USE_POSTGRES = bool(env("POSTGRES_DB")) or env_bool("DJANGO_USE_POSTGRES", False)

if USE_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB", "galileu"),
            "USER": env("POSTGRES_USER", "galileu"),
            "PASSWORD": env("POSTGRES_PASSWORD", "galileu"),
            "HOST": env("DB_HOST", "db"),
            "PORT": env("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ============================================================
# Auth
# ============================================================

AUTH_USER_MODEL = env("DJANGO_AUTH_USER_MODEL", "accounts.User")

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ============================================================
# I18N
# ============================================================

LANGUAGE_CODE = "pt-br"
TIME_ZONE = env("DJANGO_TIME_ZONE", "America/Sao_Paulo")
USE_I18N = True
USE_TZ = True

# ============================================================
# Static / Media
# ============================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# DRF
# (Sessão por cookie funciona com credentials: "include")
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

# ============================================================
# CORS / CSRF (Pages + TryCloudflare)
# ============================================================

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.pages\.dev$",
    r"^https://.*\.trycloudflare\.com$",
    r"^http://localhost(:\d+)?$",
    r"^http://127\.0\.0\.1(:\d+)?$",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.pages.dev",
    "https://*.trycloudflare.com",
]

# ============================================================
# Cookies cross-site (Somente ativa Secure quando você pedir)
# - Para funcionar no Pages -> API, você vai querer:
#   DJANGO_SECURE_COOKIES=1
# ============================================================

SECURE_COOKIES = env_bool("DJANGO_SECURE_COOKIES", False)

if SECURE_COOKIES:
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Cloudflared / proxy HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# ============================================================
# Security headers (ok para dev também)
# ============================================================

X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
REFERRER_POLICY = "strict-origin-when-cross-origin"
