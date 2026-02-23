from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# SEGURANÇA
# ==============================
# ✅ Produção: defina SECRET_KEY no ambiente (PythonAnywhere -> Web -> Environment variables)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-troque-essa-chave-depois")

# ✅ Produção: DJANGO_DEBUG=0
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

# ✅ Produção: defina DJANGO_ALLOWED_HOSTS="dominio.com, www.dominio.com"
_raw_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "matheusmarttinis.pythonanywhere.com,localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]

# Para evitar erro CSRF em HTTPS (especialmente no PythonAnywhere)
# ✅ Produção: DJANGO_CSRF_TRUSTED="https://matheusmarttinis.pythonanywhere.com"
_raw_csrf = os.environ.get("DJANGO_CSRF_TRUSTED", "")
CSRF_TRUSTED_ORIGINS = [u.strip() for u in _raw_csrf.split(",") if u.strip()]

# ==============================
# APLICAÇÕES
# ==============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "ckeditor",
    "ckeditor_uploader",

    "core",
]

# ==============================
# MIDDLEWARE
# ==============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ✅ Hardening automático quando DEBUG=False
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7  # 7 dias (pode aumentar depois)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ==============================
# TEMPLATES
# ==============================
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
                "core.context_processors.social_links",
            ],
        },
    },
]

# ==============================
# BANCO DE DADOS
# ==============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================
# VALIDAÇÃO DE SENHA
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================
# INTERNACIONALIZAÇÃO
# ==============================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ==============================
# STATIC FILES
# ==============================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ==============================
# MEDIA FILES (IMAGENS)
# ==============================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==============================
# CKEDITOR
# ==============================
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 360,
        "width": "100%",
    },
    "summary": {
        "toolbar": [
            ["Bold", "Italic", "Underline", "-", "RemoveFormat"],
            ["TextColor", "BGColor"],
            ["NumberedList", "BulletedList", "-", "Blockquote"],
            ["Link", "Unlink"],
            ["Undo", "Redo"],
            ["Source"],
        ],
        "height": 160,
        "width": "100%",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
