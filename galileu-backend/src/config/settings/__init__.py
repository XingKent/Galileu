import os

# ====== CORS para Cloudflare Pages + desenvolvimento local ======
CORS_ALLOWED_ORIGINS = [
    "https://galileu.pages.dev",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# Se você tiver outro Pages (domínio custom depois), dá pra adicionar aqui também.

# Ativa middleware CORS simples
MIDDLEWARE = ["apps.common.cors.SimpleCORSMiddleware", *MIDDLEWARE]

# ====== Cookies cross-site (Pages -> Tunnel/API) ======
# Para cookie funcionar em domínio diferente, precisa SameSite=None e Secure.
# Se isso quebrar seu DEV em http://localhost, você pode desativar depois.
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Trust para CSRF (se em algum momento o login começar a exigir CSRF)
CSRF_TRUSTED_ORIGINS = [
    "https://galileu.pages.dev",
]

# Ajuda quando existe proxy/tunnel (https fora, http dentro)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# ---- hosts ----
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

# ---- cookies cross-site (Pages -> API) ----
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "0") == "1"

if COOKIE_SECURE:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

# quando tem proxy/tunnel (https fora, http dentro)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True