from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Team, CaptainProfile, TeamMember, Robot, Certificate
from .serializers import (
    TeamSerializer, CaptainProfileSerializer,
    TeamMemberSerializer, RobotSerializer, CertificateSerializer
)


def get_or_create_team(user):
    team, _ = Team.objects.get_or_create(
        captain=user,
        defaults={"name": getattr(user, "nome", "") or getattr(user, "email", "") or "Minha Equipe"}
    )
    profile, _ = CaptainProfile.objects.get_or_create(user=user)
    return team, profile


class MyTeamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        team, profile = get_or_create_team(request.user)

        data = {
            "user": {
                "email": getattr(request.user, "email", ""),
                "nome": getattr(request.user, "nome", ""),
            },
            "profile": CaptainProfileSerializer(profile).data,
            "team": TeamSerializer(team).data,
            "members": TeamMemberSerializer(team.members.order_by("-id"), many=True).data,
            "robots": RobotSerializer(team.robots.order_by("-id"), many=True).data,
            "certificates": CertificateSerializer(team.certificates.order_by("-id"), many=True).data,
        }
        return Response(data)

    def patch(self, request):
        team, _ = get_or_create_team(request.user)

        name = request.data.get("name")
        slogan = request.data.get("slogan")

        if name is not None:
            team.name = str(name).strip()[:120]
        if slogan is not None:
            team.slogan = str(slogan).strip()[:200]

        team.save()
        return Response(TeamSerializer(team).data)


class UploadCaptainPhotoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        _, profile = get_or_create_team(request.user)
        f = request.FILES.get("photo")
        if not f:
            return Response({"detail": "Envie o arquivo no campo 'photo'."}, status=400)

        profile.photo = f
        profile.save()
        return Response(CaptainProfileSerializer(profile).data, status=200)


class UploadTeamLogoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        team, _ = get_or_create_team(request.user)
        f = request.FILES.get("logo")
        if not f:
            return Response({"detail": "Envie o arquivo no campo 'logo'."}, status=400)

        team.logo = f
        team.save()
        return Response(TeamSerializer(team).data, status=200)


class MemberListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamMemberSerializer

    def get_queryset(self):
        team, _ = get_or_create_team(self.request.user)
        return TeamMember.objects.filter(team=team).order_by("-id")

    def perform_create(self, serializer):
        team, _ = get_or_create_team(self.request.user)
        serializer.save(team=team)


class MemberDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamMemberSerializer

    def get_queryset(self):
        team, _ = get_or_create_team(self.request.user)
        return TeamMember.objects.filter(team=team)


class RobotListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RobotSerializer

    def get_queryset(self):
        team, _ = get_or_create_team(self.request.user)
        return Robot.objects.filter(team=team).order_by("-id")

    def perform_create(self, serializer):
        team, _ = get_or_create_team(self.request.user)
        serializer.save(team=team)


class RobotDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RobotSerializer

    def get_queryset(self):
        team, _ = get_or_create_team(self.request.user)
        return Robot.objects.filter(team=team)


class CertificateListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CertificateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        team, _ = get_or_create_team(self.request.user)
        return Certificate.objects.filter(team=team).order_by("-id")

    def create(self, request, *args, **kwargs):
        team, _ = get_or_create_team(request.user)

        title = (request.data.get("title") or "").strip()
        f = request.FILES.get("file")

        if not title:
            return Response({"detail": "Campo 'title' é obrigatório."}, status=400)
        if not f:
            return Response({"detail": "Envie o arquivo no campo 'file'."}, status=400)

        cert = Certificate.objects.create(team=team, title=title, file=f)
        return Response(CertificateSerializer(cert).data, status=201)


class CertificateDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CertificateSerializer

    def get_queryset(self):
        team, _ = get_or_create_team(self.request.user)
        return Certificate.objects.filter(team=team)
