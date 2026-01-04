from rest_framework import serializers
from .models import Team, CaptainProfile, TeamMember, Robot, Certificate


class TeamSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["id", "name", "slogan", "created_at", "logo_url"]

    def get_logo_url(self, obj):
        return obj.logo.url if obj.logo else None


class CaptainProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = CaptainProfile
        fields = ["photo_url"]

    def get_photo_url(self, obj):
        return obj.photo.url if obj.photo else None


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["id", "name", "email", "created_at"]


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ["id", "name", "created_at"]


class CertificateSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = ["id", "title", "file_url", "created_at"]

    def get_file_url(self, obj):
        return obj.file.url if obj.file else None
