import os
from .base import * # <--- ESTA ERA A LINHA QUE FALTAVA!

# Agora que importamos o 'base', o Python já conhece a variável MIDDLEWARE

# ====== CORS para Cloudflare Pages + desenvolvimento local ======
CORS_ALLOWED_ORIGINS = [
    "https://galileu.pages.dev",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# Adiciona o middleware de CORS no topo da lista existente
MIDDLEWARE = ["apps.common.cors.SimpleCORSMiddleware", *MIDDLEWARE]

# ---- hosts ----
# Pega os hosts do ambiente ou usa padrão local
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,revelation-deutschland-clearance-label.trycloudflare.com").split(",") if h.strip()]
# Adicionei o trycloudflare.com no padrão ali em cima para garantir

# ---- Configurações de Segurança e Cookies (Unificado) ----
# Verifica se estamos forçando segurança via variável de ambiente
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "0") == "1"

if COOKIE_SECURE:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
else:
    # Em desenvolvimento local (HTTP), não pode ser Secure
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_HTTPONLY = True

# Confiança CSRF (Juntando suas duas listas)
CSRF_TRUSTED_ORIGINS_ENV = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]
CSRF_TRUSTED_ORIGINS = [
    "https://galileu.pages.dev",
    "https://*.trycloudflare.com", # Dica: Aceita qualquer túnel, evita ter que mudar sempre
] + CSRF_TRUSTED_ORIGINS_ENV

# Ajuda quando existe proxy/tunnel (https fora, http dentro)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True