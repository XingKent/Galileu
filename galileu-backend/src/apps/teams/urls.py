from django.urls import path
from .views import (
    MyTeamView,
    UploadCaptainPhotoView,
    UploadTeamLogoView,
    MemberListCreateView, MemberDeleteView,
    RobotListCreateView, RobotDeleteView,
    CertificateListCreateView, CertificateDeleteView,
)

urlpatterns = [
    path("me/", MyTeamView.as_view()),
    path("captain/photo/", UploadCaptainPhotoView.as_view()),
    path("logo/", UploadTeamLogoView.as_view()),

    path("members/", MemberListCreateView.as_view()),
    path("members/<int:pk>/", MemberDeleteView.as_view()),

    path("robots/", RobotListCreateView.as_view()),
    path("robots/<int:pk>/", RobotDeleteView.as_view()),

    path("certificates/", CertificateListCreateView.as_view()),
    path("certificates/<int:pk>/", CertificateDeleteView.as_view()),
    path("api/team/", include("apps.teams.urls")),
]
