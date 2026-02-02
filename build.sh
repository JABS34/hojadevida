#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Archivos estáticos
python manage.py collectstatic --no-input

# 3. Aplicar tablas a PostgreSQL
python manage.py migrate

# 4. CREAR SUPERUSUARIO (Todo en una sola línea)
# Cambia 'TuPasswordAqui' por la que tú quieras
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='jabs6393').exists() or User.objects.create_superuser('jabs6393', 'admin@ejemplo.com', 'jonathan100.')"

# 5. Permisos de carpetas
mkdir -p media
chmod -R 755 media
