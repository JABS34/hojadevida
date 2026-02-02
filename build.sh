#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# GENERAR MIGRACIONES FALTANTES (Esto arregla el error 500)
python manage.py makemigrations

# APLICAR MIGRACIONES
python manage.py migrate

# Crear carpeta de fotos si no existe
mkdir -p media
chmod -R 755 media
