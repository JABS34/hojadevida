from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    Habilidad, Certificado, Educacion, Lenguaje, 
    ProductoGarage, Reconocimiento
)

# Configuración de Datos Personales
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'user')
    search_fields = ('nombres', 'apellidos')

# Configuración del Garage
@admin.register(ProductoGarage)
class ProductoGarageAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponible', 'fecha_publicado')
    list_filter = ('disponible', 'fecha_publicado')
    list_editable = ('disponible', 'precio')
    search_fields = ('nombre',)

# Registro simple para los demás modelos (evita errores de columnas)
admin.site.register(Task)
admin.site.register(ExperienciaLaboral)
admin.site.register(Habilidad)
admin.site.register(Certificado)
admin.site.register(Educacion)
admin.site.register(Lenguaje)
admin.site.register(Reconocimiento)
