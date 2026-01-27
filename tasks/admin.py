from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    Habilidad, Certificado, Educacion, Lenguaje, 
    ProductoGarage, Reconocimiento
)

# --- Registro simplificado (A prueba de errores) ---

# Usamos el registro básico para estos modelos. 
# Esto hará que Django use los nombres por defecto y NO falle el despliegue.
admin.site.register(Task)
admin.site.register(Habilidad)
admin.site.register(Lenguaje)
admin.site.register(Reconocimiento)
admin.site.register(Certificado) # Sin clase Admin para evitar el error 'nombre'
admin.site.register(ExperienciaLaboral) # Sin clase Admin para evitar error de fechas
admin.site.register(Educacion)

class DatosPersonalesAdmin(admin.ModelAdmin):
    # Solo nombres y apellidos que son campos estándar
    list_display = ('nombres', 'apellidos', 'user')
    search_fields = ('nombres', 'apellidos')

class ProductoGarageAdmin(admin.ModelAdmin):
    # Solo nombre y precio para asegurar que el build pase
    list_display = ('nombre', 'precio', 'disponible')
    list_editable = ('disponible', 'precio')

admin.site.register(DatosPersonales, DatosPersonalesAdmin)
admin.site.register(ProductoGarage, ProductoGarageAdmin)
