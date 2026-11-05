"""
Django settings for Dawra Campus.

Local development reads src/.env (copy .env.example). Render sets the same names as
environment variables. Without DATABASE_URL the app uses a local SQLite file, and
without ANTHROPIC_API_KEY it runs with the AI features marked unavailable.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes")


DEBUG = env_bool("DEBUG", False)
SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError("Set SECRET_KEY in the environment (see src/.env.example).")
    SECRET_KEY = "dev-only-key-not-for-production"

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]
if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(os.environ["RENDER_EXTERNAL_HOSTNAME"])
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if "." in h and not h[0].isdigit()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Dawra Campus apps, one per part of the component diagram (design section 11)
    "accounts",           # Security: sign-in, roles and department checks
    "core",               # Pages and forms: layout and home page
    "assets",             # Business workflows: assets, listings and search
    "resource_requests",  # Business workflows: resource requests
    "transfers",          # Business workflows: approvals, holds and transfers
    "audit",              # Data and audit access: state rules and history
    "notifications",      # Notifications: in-app updates
    "sustainability",     # Reporting: sustainability indicators
    "reports",            # Reporting: request and transfer report with CSV
    "ai",                 # AI adapter and AI services
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "accounts.middleware.ActiveRoleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dawra.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.active_role",
            ],
        },
    },
]

WSGI_APPLICATION = "dawra.wsgi.application"

if os.environ.get("DATABASE_URL"):
    DATABASES = {"default": dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600)}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "accounts:login"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Section 6: sessions end after 30 minutes without activity.
SESSION_COOKIE_AGE = 30 * 60
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Asia/Dubai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Business rules and thresholds from the Phase 3 SRS (Appendix TBD list).
DAWRA = {
    # TBD-1 is still "KU Finance to set"; AED 5,000 is our prototype value.
    "FINANCE_APPROVAL_THRESHOLD_AED": float(os.environ.get("FINANCE_APPROVAL_THRESHOLD_AED", "5000")),
    "HOLD_WORKING_DAYS": 5,          # TBD-3, BR-12
    "VERIFICATION_MAX_AGE_DAYS": 90,  # TBD-4, BR-16
    "OVERDUE_WORKING_DAYS": 3,       # TBD-5, FR-10.5
    "MAX_FAILED_SIGN_INS": 5,        # section 6
    "LOCKOUT_MINUTES": 15,           # section 6
}

# AI settings (design section 4, changed to the Claude API in Phase 6).
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
AI = {
    "CLASSIFICATION_MODEL": "claude-haiku-5-5",
    "MATCHING_MODEL": "claude-haiku-5-5",
    "REPORT_MODEL": "claude-sonnet-5-5",
    "DEADLINE_SECONDS": 15,           # AI-13.2: one 15-second limit per user request
    "CLASSIFICATION_RUNS": 3,         # confidence = share of runs that agree
    "CLASSIFICATION_THRESHOLD": 0.60,  # SRS Table 4.2
    "MATCH_SHOW_NORMALLY": 0.75,      # SRS Table 4.2
    "MATCH_CHECK_CAREFULLY": 0.50,    # SRS Table 4.2
    "MATCHES_SHOWN": 5,               # Phase 6 brief: top 5 surplus items
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"dawra.ai": {"handlers": ["console"], "level": "INFO"}},
}
