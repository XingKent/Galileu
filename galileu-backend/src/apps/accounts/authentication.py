from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Autentica usando:
    1) Authorization: Bearer <token> (padrão)
    2) Cookie HttpOnly: access_token (para navegador)
    """

    def authenticate(self, request):
        # Se veio Authorization header, usa o fluxo padrão do SimpleJWT
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)

        # Caso contrário, tenta pegar do cookie (fluxo do navegador)
        raw_token = request.COOKIES.get("access_token")
        if not raw_token:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
