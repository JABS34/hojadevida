from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    Habilidad, Certificado, Educacion, Lenguaje, 
    ProductoGarage, Reconocimiento
)

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'user', 'numerocedula')
    search_fields = ('nombres', 'apellidos', 'numerocedula')

@admin.register(ProductoGarage)
class ProductoGarageAdmin(admin.ModelAdmin):
    # Ahora incluimos 'estado' en la visualización
    list_display = ('nombre', 'precio', 'estado', 'disponible', 'fecha_publicado')
    list_filter = ('disponible', 'estado', 'fecha_publicado')
    list_editable = ('disponible', 'precio', 'estado')
    search_fields = ('nombre', 'descripcion')

@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion_otorga', 'fecha', 'perfil')

admin.site.register(Task)
admin.site.register(Certificado)
admin.site.register(ExperienciaLaboral)
admin.site.register(Habilidad)
admin.site.register(Educacion)
admin.site.register(Lenguaje)
