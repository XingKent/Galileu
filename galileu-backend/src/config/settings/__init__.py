import os

# Esse arquivo escolhe automaticamente dev ou prod
env = os.getenv("DJANGO_ENV", "dev")

if env == "prod":
    from .prod import *  # noqa
else:
    from .dev import *  # noqa
