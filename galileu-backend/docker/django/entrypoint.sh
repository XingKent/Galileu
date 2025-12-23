#!/usr/bin/env bash
set -e

# Sobe o banco / migra / gera estáticos e roda o gunicorn
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Gunicorn em produção (serve API)
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 60
