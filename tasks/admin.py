from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    Habilidad, Certificado, Educacion, Lenguaje, 
    ProductoGarage # Importamos el nuevo modelo
)

class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'user')
    search_fields = ('nombres', 'apellidos', 'numerocedula')

class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'fecha_obtencion', 'perfil')
    list_filter = ('institucion',)

class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('puesto', 'empresa', 'fecha_inicio', 'actualidad')

class EducacionAdmin(admin.ModelAdmin):
    list_display = ('institucion', 'fecha_graduacion', 'perfil')
    list_filter = ('institucion',)

class LenguajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'perfil')

# --- Nueva configuración para la Venta de Garage ---
class ProductoGarageAdmin(admin.ModelAdmin):
    # Esto muestra columnas útiles en la lista del admin
    list_display = ('nombre', 'precio', 'estado', 'disponible', 'fecha_publicado')
    # Permite filtrar por estado o disponibilidad en el lateral
    list_filter = ('estado', 'disponible', 'fecha_publicado')
    # Permite buscar productos por nombre
    search_fields = ('nombre', 'descripcion')
    # Permite editar la disponibilidad directamente desde la lista sin entrar al producto
    list_editable = ('disponible', 'precio')

admin.site.register(Task)
admin.site.register(DatosPersonales, DatosPersonalesAdmin)
admin.site.register(ExperienciaLaboral, ExperienciaAdmin)
admin.site.register(Habilidad)
admin.site.register(Certificado, CertificadoAdmin)
admin.site.register(Educacion, EducacionAdmin)
admin.site.register(Lenguaje, LenguajeAdmin)

# Registramos el nuevo modelo con su configuración
admin.site.register(ProductoGarage, ProductoGarageAdmin)
