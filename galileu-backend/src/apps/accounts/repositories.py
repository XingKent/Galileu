from django.contrib.auth import get_user_model

User = get_user_model()

class UserRepository:
    # Repositório: só acesso a dados (ORM). Não faz regra de negócio.
    def get_by_email(self, email: str):
        return User.objects.filter(email=email).first()

    def get_by_cpf(self, cpf: str):
        return User.objects.filter(cpf=cpf).first()

    def create(self, **data):
        password = data.pop("password")
        return User.objects.create_user(password=password, **data)
