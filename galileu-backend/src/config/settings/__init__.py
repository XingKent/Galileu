import os
from .base import * # <--- Importa as configurações originais

# ====== 1. CORS (Quem pode acessar) ======
CORS_ALLOWED_ORIGINS = [
    "https://galileu.pages.dev",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]


# ====== 2. Hosts Permitidos (Quem é o servidor) ======
ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "ALLOWED_HOSTS", 
    "localhost,127.0.0.1,.trycloudflare.com,revelation-deutschland-clearance-label.trycloudflare.com"
).split(",") if h.strip()]

# ====== 3. Segurança e Cookies (Unificado) ======
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "0") == "1"

if COOKIE_SECURE:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
else:
    # Em desenvolvimento local, precisa ser False/Lax
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_HTTPONLY = True

# ====== 4. CSRF (Confiança na Origem) ======
CSRF_TRUSTED_ORIGINS_ENV = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

CSRF_TRUSTED_ORIGINS = [
    "https://galileu.pages.dev",
    "https://*.trycloudflare.com", # Aceita qualquer túnel (Importante!)
] + CSRF_TRUSTED_ORIGINS_ENV

# ====== 5. Proxy (Para funcionar HTTPS atrás do Cloudflare) ======
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True