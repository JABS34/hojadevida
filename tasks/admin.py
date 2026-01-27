from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    Habilidad, Certificado, Educacion, Lenguaje, 
    ProductoGarage, Reconocimiento
)

# 1. Configuración de Datos Personales
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'user', 'numerocedula')
    search_fields = ('nombres', 'apellidos', 'numerocedula')

# 2. Configuración de la Venta de Garage (Soluciona el Error 500)
@admin.register(ProductoGarage)
class ProductoGarageAdmin(admin.ModelAdmin):
    # Usamos exactamente los nombres del modelo: nombre, precio, disponible, fecha_publicado
    list_display = ('nombre', 'precio', 'disponible', 'fecha_publicado')
    list_filter = ('disponible', 'fecha_publicado')
    list_editable = ('disponible', 'precio')
    search_fields = ('nombre', 'descripcion')

# 3. Configuración de Reconocimientos (Para que se vea bien el título)
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion_otorga', 'fecha', 'perfil')
    list_filter = ('fecha', 'institucion_otorga')
    search_fields = ('titulo', 'descripcion')

# 4. Configuración de Certificados
@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'perfil')
    search_fields = ('titulo', 'institucion')

# 5. Configuración de Experiencia Laboral
@admin.register(ExperienciaLaboral)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('puesto', 'empresa', 'perfil')
    search_fields = ('puesto', 'empresa')

# 6. Registros Simples (Para modelos con pocos campos)
admin.site.register(Task)
admin.site.register(Habilidad)
admin.site.register(Educacion)
admin.site.register(Lenguaje)
