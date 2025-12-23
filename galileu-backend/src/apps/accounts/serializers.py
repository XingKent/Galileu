from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nome = serializers.CharField(max_length=200)
    nascimento = serializers.DateField(required=False, allow_null=True)
    cpf = serializers.CharField(required=False, allow_blank=True)
    telefone = serializers.CharField(required=False, allow_blank=True)
    senha = serializers.CharField(min_length=8, write_only=True)
    confirmar = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        if attrs["senha"] != attrs["confirmar"]:
            raise serializers.ValidationError("Senhas não conferem")
        return attrs

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)

class MeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nome = serializers.CharField()
