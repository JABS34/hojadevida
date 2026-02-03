from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    CursosRealizados, Reconocimiento, VentaGarage,
    ProductosAcademicos, ProductosLaborales,
    LenguajeProgramacion, Habilidad, ConfiguracionVisible
)

# 1. TAREAS
admin.site.register(Task)

# 2. DATOS PERSONALES
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'user', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 3. CONFIGURACIÓN DE BOTONES (VISIBILIDAD)
@admin.register(ConfiguracionVisible)
class ConfiguracionVisibleAdmin(admin.ModelAdmin):
    list_display = ('idperfilconqueestaactivo', 'mostrar_garage', 'mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_editar')
    list_editable = ('mostrar_garage', 'mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_editar')

# 4. EXPERIENCIA LABORAL
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 5. RECONOCIMIENTOS
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'entidadpatrocinadora', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 6. CURSOS
@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'entidadpatrocinadora', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 7. PRODUCTOS ACADÉMICOS
@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 8. PRODUCTOS LABORALES
@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 9. GARAGE
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 10. LENGUAJES
@admin.register(LenguajeProgramacion)
class LenguajeProgramacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_porcentaje', 'activarparaqueseveaenfront')
    list_editable = ('nivel_porcentaje', 'activarparaqueseveaenfront')

# 11. HABILIDADES
@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre_habilidad', 'categoria', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)