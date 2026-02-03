from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    CursosRealizados, Reconocimiento, VentaGarage,
    ProductosAcademicos, ProductosLaborales,
    LenguajeProgramacion, Habilidad, ConfiguracionVisible
)

# Registros Simples
admin.site.register(Task)

# Registros con visualización avanzada
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'user', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(ConfiguracionVisible)
class ConfiguracionVisibleAdmin(admin.ModelAdmin):
    list_display = ('idperfilconqueestaactivo', 'mostrar_garage', 'mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_editar')
    list_editable = ('mostrar_garage', 'mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_editar')

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(LenguajeProgramacion)
class LenguajeProgramacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_porcentaje', 'activarparaqueseveaenfront')
    list_editable = ('nivel_porcentaje', 'activarparaqueseveaenfront')

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre_habilidad', 'categoria', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)