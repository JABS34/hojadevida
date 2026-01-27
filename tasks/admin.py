from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    Habilidad, Certificado, Educacion, Lenguaje, 
    ProductoGarage, Reconocimiento # Añadido Reconocimiento para evitar fallos
)

class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'user')
    search_fields = ('nombres', 'apellidos')

class CertificadoAdmin(admin.ModelAdmin):
    # Se eliminó 'fecha_obtencion' porque el modelo no reconoce ese nombre
    list_display = ('nombre', 'institucion', 'perfil') 
    list_filter = ('institucion',)

class ExperienciaAdmin(admin.ModelAdmin):
    # Se eliminaron 'fecha_inicio' y 'actualidad' por errores de nombre
    list_display = ('puesto', 'empresa', 'perfil')

class EducacionAdmin(admin.ModelAdmin):
    list_display = ('institucion', 'perfil')
    list_filter = ('institucion',)

class LenguajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'perfil')

class ProductoGarageAdmin(admin.ModelAdmin):
    # Se eliminó 'estado' porque tu modelo usa 'disponible'
    list_display = ('nombre', 'precio', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('disponible', 'precio')

# Registro de modelos
admin.site.register(Task)
admin.site.register(DatosPersonales, DatosPersonalesAdmin)
admin.site.register(ExperienciaLaboral, ExperienciaAdmin)
admin.site.register(Habilidad)
admin.site.register(Certificado, CertificadoAdmin)
admin.site.register(Educacion, EducacionAdmin)
admin.site.register(Lenguaje, LenguajeAdmin)
admin.site.register(ProductoGarage, ProductoGarageAdmin)
admin.site.register(Reconocimiento) # Importante para que no falle el CV
