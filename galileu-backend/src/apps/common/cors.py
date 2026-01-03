import re
from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class SimpleCORSMiddleware(MiddlewareMixin):
    """
    CORS simples para liberar o front (Cloudflare Pages) chamando a API via tunnel.
    - Responde preflight (OPTIONS) com 204
    - Adiciona headers CORS em todas as respostas
    """

    def _is_allowed_origin(self, origin: str) -> bool:
        if not origin:
            return False

        allowed = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
        if origin in allowed:
            return True

        regexes = getattr(settings, "CORS_ALLOWED_ORIGIN_REGEXES", [])
        for rx in regexes:
            if re.match(rx, origin):
                return True

        return False

    def _add_headers(self, request, response):
        origin = request.headers.get("Origin")
        if origin and self._is_allowed_origin(origin):
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
        return response

    def process_request(self, request):
        if request.method == "OPTIONS":
            resp = HttpResponse(status=204)
            return self._add_headers(request, resp)
        return None

    def process_response(self, request, response):
        return self._add_headers(request, response)
