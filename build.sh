#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Crear los archivos de migración que faltan para la tabla 'tasks_configuracionvisible'
python manage.py makemigrations tasks --noinput

# Aplicar los cambios a la base de datos de Render
python manage.py migrate --noinput

# Crear el superusuario automáticamente (usa las variables de entorno de Render)
# Asegúrate de tener DJANGO_SUPERUSER_USERNAME y DJANGO_SUPERUSER_PASSWORD en Render
python manage.py createsuperuser --noinput || true
