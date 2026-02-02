#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# GENERAR Y APLICAR MIGRACIONES
python manage.py makemigrations
python manage.py migrate

# Solo intentar crear la carpeta media si el disco está montado
if [ -d "/data" ]; then
    mkdir -p /data/media
    chmod -R 755 /data/media || true
fi
