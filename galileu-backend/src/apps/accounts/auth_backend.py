from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailBackend(ModelBackend):
    # Permite login usando email + senha no authenticate()
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get("email") or username
        if not email or not password:
            return None

        user = User.objects.filter(email=email).first()
        if not user:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
