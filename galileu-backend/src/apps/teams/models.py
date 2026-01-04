from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Team(models.Model):
    captain = models.OneToOneField(User, on_delete=models.CASCADE, related_name="team")
    name = models.CharField(max_length=120, default="Minha Equipe")
    slogan = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateField(auto_now_add=True)
    logo = models.ImageField(upload_to="team/logos/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.captain_id})"


class CaptainProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="captain_profile")
    photo = models.ImageField(upload_to="captain/photos/", blank=True, null=True)

    def __str__(self):
        return f"Profile({self.user_id})"


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)


class Robot(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="robots")
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)


class Certificate(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="certificates")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="team/certificates/")
    created_at = models.DateTimeField(auto_now_add=True)
