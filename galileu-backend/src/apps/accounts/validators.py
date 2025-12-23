import re

def normalize_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")

def validate_cpf(value: str) -> str:
    # Aqui é validação simples (tamanho). Depois dá pra colocar algoritmo do CPF.
    digits = normalize_digits(value)
    if len(digits) != 11:
        raise ValueError("CPF inválido")
    return digits

def validate_phone(value: str) -> str:
    digits = normalize_digits(value)
    if len(digits) < 10 or len(digits) > 13:
        raise ValueError("Telefone inválido")
    return digits
