#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Archivos estáticos
python manage.py collectstatic --no-input

# 3. Permisos básicos
mkdir -p media
chmod -R 755 media
