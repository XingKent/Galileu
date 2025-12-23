from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, MeSerializer
from .services import AuthService

def _set_auth_cookies(response: Response, refresh: RefreshToken, secure: bool):
    # Guardar token em cookie HttpOnly reduz o risco de JS roubar o token (XSS)
    response.set_cookie(
        "access_token",
        str(refresh.access_token),
        httponly=True,
        secure=secure,
        samesite="Lax",
        max_age=15 * 60,
    )
    response.set_cookie(
        "refresh_token",
        str(refresh),
        httponly=True,
        secure=secure,
        samesite="Lax",
        max_age=7 * 24 * 60 * 60,
    )

def _is_secure_request(request) -> bool:
    # Em localhost a gente aceita sem HTTPS
    host = request.get_host() or ""
    if "localhost" in host or "127.0.0.1" in host:
        return False
    return True

class RegisterApi(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        service = AuthService()
        data = ser.validated_data

        try:
            user = service.register(
                email=data["email"],
                nome=data["nome"],
                nascimento=data.get("nascimento"),
                cpf=(data.get("cpf") or None),
                telefone=(data.get("telefone") or None),
                password=data["senha"],
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        resp = Response({"ok": True}, status=status.HTTP_201_CREATED)
        _set_auth_cookies(resp, refresh, secure=_is_secure_request(request))
        return resp

class LoginApi(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        service = AuthService()

        try:
            user = service.login(
                email=ser.validated_data["email"],
                password=ser.validated_data["senha"],
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        resp = Response({"ok": True}, status=status.HTTP_200_OK)
        _set_auth_cookies(resp, refresh, secure=_is_secure_request(request))
        return resp

class LogoutApi(APIView):
    def post(self, request):
        resp = Response({"ok": True}, status=status.HTTP_200_OK)
        resp.delete_cookie("access_token")
        resp.delete_cookie("refresh_token")
        return resp

class MeApi(APIView):
    def get(self, request):
        data = {"email": request.user.email, "nome": request.user.nome}
        return Response(MeSerializer(data).data, status=status.HTTP_200_OK)
