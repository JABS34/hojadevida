#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Esto creará la tabla 'tasks_configuracionvisible' en PostgreSQL
python manage.py migrate

# Crea tu usuario (Usa una contraseña que no tenga puntos al final, ej: jabs123)
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='jabs6393').exists() or User.objects.create_superuser('jabs6393', '', '1111')"

mkdir -p media
chmod -R 755 media
