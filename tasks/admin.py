from django.contrib import admin
from .models import Task, DatosPersonales, ExperienciaLaboral, Habilidad, Certificado, Educacion, Lenguaje

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

admin.site.register(Task)
admin.site.register(DatosPersonales, DatosPersonalesAdmin)
admin.site.register(ExperienciaLaboral, ExperienciaAdmin)
admin.site.register(Habilidad)
admin.site.register(Certificado, CertificadoAdmin)
admin.site.register(Educacion, EducacionAdmin)
admin.site.register(Lenguaje, LenguajeAdmin)