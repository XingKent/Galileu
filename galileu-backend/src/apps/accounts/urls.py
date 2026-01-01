from django.urls import path
from .views import RegisterApi, LoginApi, LogoutApi, MeApi

urlpatterns = [
    path("register/", RegisterApi.as_view(), name="register"),
    path("login/", LoginApi.as_view(), name="login"),
    path("logout/", LogoutApi.as_view(), name="logout"),
    path("me/", MeApi.as_view(), name="me"),
    
]
