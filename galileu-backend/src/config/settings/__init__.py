import os
from .base import * # ====== 1. Configuração do CORS (O Coração do problema) ======
# Define QUEM pode acessar (Não use '*' aqui se usar Credentials)
CORS_ALLOWED_ORIGINS = [
    "https://galileu.pages.dev",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# (NOVO) Isso é OBRIGATÓRIO quando o frontend manda cookies/login
CORS_ALLOW_CREDENTIALS = True

# O Middleware correto (tem que ser o primeiro da lista extra)
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", *MIDDLEWARE]

# ====== 2. Hosts Permitidos (Quem sou eu) ======
ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "ALLOWED_HOSTS", 
    "localhost,127.0.0.1,.trycloudflare.com,revelation-deutschland-clearance-label.trycloudflare.com"
).split(",") if h.strip()]

# ====== 3. Segurança de Cookies (HTTPS vs HTTP) ======
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "0") == "1"

if COOKIE_SECURE:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
else:
    # Em desenvolvimento, deixa False para não travar
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_HTTPONLY = True

# ====== 4. CSRF (Confiança na Origem) ======
CSRF_TRUSTED_ORIGINS_ENV = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

CSRF_TRUSTED_ORIGINS = [
    "https://galileu.pages.dev",
    "https://*.trycloudflare.com", 
] + CSRF_TRUSTED_ORIGINS_ENV

# ====== 5. Proxy (Cloudflare HTTPS) ======
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True