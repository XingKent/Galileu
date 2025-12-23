from django.contrib.auth import authenticate
from .repositories import UserRepository
from .validators import validate_cpf, validate_phone

class AuthService:
    # Service: regra de negócio (cadastro/login), chamando repository
    def __init__(self, repo: UserRepository | None = None):
        self.repo = repo or UserRepository()

    def register(self, *, email, nome, nascimento=None, cpf=None, telefone=None, password=None):
        if self.repo.get_by_email(email):
            raise ValueError("Email já cadastrado")

        if cpf:
            cpf = validate_cpf(cpf)
            if self.repo.get_by_cpf(cpf):
                raise ValueError("CPF já cadastrado")

        if telefone:
            telefone = validate_phone(telefone)

        return self.repo.create(
            email=email,
            nome=nome,
            nascimento=nascimento,
            cpf=cpf,
            telefone=telefone,
            password=password,
        )

    def login(self, *, email, password):
        # authenticate usa o backend do Django
        user = authenticate(email=email, password=password)
        if not user:
            raise ValueError("Credenciais inválidas")
        return user
