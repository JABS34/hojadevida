#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Esto crea las tablas en la base de datos de Render (PostgreSQL)
python manage.py migrate --noinput

# Crea el superusuario jabs6393 (Contraseña: jabs12345)
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='jabs6393').exists() or User.objects.create_superuser('jabs6393', 'admin@ejemplo.com', 'jabs12345')"

mkdir -p media
chmod -R 755 media
