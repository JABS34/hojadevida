#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# 1. Aplicar tablas a PostgreSQL
python manage.py migrate --noinput

# 2. Crear superusuario usando variables de entorno
# El flag --noinput leerá las variables que configuraremos en el siguiente paso
python manage.py createsuperuser --noinput || true

mkdir -p media
chmod -R 755 media
