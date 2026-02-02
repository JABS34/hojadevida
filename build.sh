#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Generar y aplicar migraciones para evitar el error 500
python manage.py makemigrations
python manage.py migrate

# Carpeta de fotos
mkdir -p media
chmod -R 755 media
