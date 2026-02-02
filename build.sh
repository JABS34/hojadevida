#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar librerías
pip install -r requirements.txt

# Preparar archivos estáticos
python manage.py collectstatic --no-input

# Crear y aplicar tablas en la base de datos PostgreSQL
python manage.py makemigrations
python manage.py migrate

# Carpeta para fotos
mkdir -p media
chmod -R 755 media
