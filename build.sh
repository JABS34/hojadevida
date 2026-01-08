#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos (CSS, JS)
python manage.py collectstatic --no-input

# Aplicar migraciones de base de datos
python manage.py migrate

# CREAR CARPETA DE FOTOS Y DAR PERMISOS
# Esto evita que salga el cuadro roto por falta de acceso
mkdir -p media
chmod -R 755 media