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
    list_display = ('nombres', 'apellidos', 'numerocedula', 'nacionalidad', 'user', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('nombres', 'apellidos', 'numerocedula')

# 3. CONFIGURACIÓN DE VISIBILIDAD (NUEVO)
@admin.register(ConfiguracionVisible)
class ConfiguracionVisibleAdmin(admin.ModelAdmin):
    list_display = ('idperfilconqueestaactivo', 'mostrar_garage', 'mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_editar')
    list_editable = ('mostrar_garage', 'mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_editar')

# 4. EXPERIENCIA LABORAL
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'fechafingestion', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('cargodesempenado', 'nombrempresa')

# 5. RECONOCIMIENTOS
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'entidadpatrocinadora', 'tiporeconocimiento', 'activarparaqueseveaenfront')
    list_filter = ('tiporeconocimiento', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 6. CURSOS REALIZADOS
@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'entidadpatrocinadora', 'totalhoras', 'fechafin', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('nombrerecurso', 'entidadpatrocinadora')

# 7. PRODUCTOS ACADÉMICOS
@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 8. PRODUCTOS LABORALES
@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_filter = ('fechaproducto',)
    list_editable = ('activarparaqueseveaenfront',)

# 9. VENTA GARAGE
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')
    list_editable = ('valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    search_fields = ('nombreproducto',)

# 10. LENGUAJES DE PROGRAMACIÓN
@admin.register(LenguajeProgramacion)
class LenguajeProgramacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_porcentaje', 'idperfilconqueestaactivo', 'activarparaqueseveaenfront')
    list_editable = ('nivel_porcentaje', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront',)

# 11. HABILIDADES
@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre_habilidad', 'categoria', 'idperfilconqueestaactivo', 'activarparaqueseveaenfront')
    list_filter = ('categoria', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)