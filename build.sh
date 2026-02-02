#!/usr/bin/env bash
set -o errexit

# Instalar librerías
pip install -r requirements.txt

# Archivos estáticos
python manage.py collectstatic --no-input

# Crear las tablas en la base de datos nueva
python manage.py migrate

# Asegurar carpeta de imágenes
mkdir -p media
chmod -R 755 media
