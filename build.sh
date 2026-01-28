#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# GENERAR Y APLICAR MIGRACIONES (Paso crítico)
python manage.py makemigrations
python manage.py migrate

# CREAR CARPETA DE FOTOS
mkdir -p media
chmod -R 755 media
