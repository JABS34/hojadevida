#!/usr/bin/env bash
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# --- PASOS CRÍTICOS PARA LA BASE DE DATOS ---
# 1. Forzar la creación de archivos de migración para tu app 'tasks'
python manage.py makemigrations auth
python manage.py makemigrations tasks

# 2. Aplicar las migraciones (crear las tablas de verdad en Postgres)
python manage.py migrate --noinput

# 3. Crear el superusuario (usando estas variables fijas para no fallar)
# Si prefieres, cámbialas aquí mismo directamente
export DJANGO_SUPERUSER_USERNAME=jabs6393
export DJANGO_SUPERUSER_PASSWORD=jabs12345

python manage.py createsuperuser --noinput || true
