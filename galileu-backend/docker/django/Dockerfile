FROM python:3.12-slim

# Evita gerar .pyc e deixa logs mais "reais" no docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependências comuns (psycopg2 precisa das libs do postgres)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential libpq-dev curl bash \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala libs do projeto (fixando versões pra não quebrar do nada)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
      django==5.0.10 \
      djangorestframework==3.15.2 \
      djangorestframework-simplejwt==5.3.1 \
      psycopg2-binary==2.9.9 \
      django-environ==0.11.2 \
      django-cors-headers==4.4.0 \
      gunicorn==22.0.0

# Entry do container (vai ser montado via volume, mas deixo a rota padrão)
COPY docker/django/entrypoint.sh /entrypoint.sh

EXPOSE 8000
