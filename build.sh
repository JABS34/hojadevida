#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Crear carpetas en el DISCO PERSISTENTE de Render
if [ "$RENDER" ]; then
  mkdir -p /data/media
fi

# Generar y aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Asegurar permisos
chmod -R 755 media || true
