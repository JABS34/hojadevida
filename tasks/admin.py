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

# 3. EXPERIENCIA LABORAL
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'fechafingestion', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    search_fields = ('cargodesempenado', 'nombrempresa')
    list_editable = ('activarparaqueseveaenfront',)

# 4. RECONOCIMIENTOS
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'entidadpatrocinadora', 'tiporeconocimiento', 'fechareconocimiento', 'activarparaqueseveaenfront')
    list_filter = ('tiporeconocimiento', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 5. CURSOS REALIZADOS
@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'entidadpatrocinadora', 'totalhoras', 'fechafin', 'activarparaqueseveaenfront')
    search_fields = ('nombrerecurso', 'entidadpatrocinadora')
    list_editable = ('activarparaqueseveaenfront',)

# 6. PRODUCTOS ACADÉMICOS
@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 7. PRODUCTOS LABORALES
@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_filter = ('fechaproducto',)
    list_editable = ('activarparaqueseveaenfront',)

# 8. VENTA GARAGE
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')
    list_editable = ('valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    search_fields = ('nombreproducto',)   

# 9. LENGUAJES DE PROGRAMACIÓN
@admin.register(LenguajeProgramacion)
class LenguajeProgramacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_porcentaje', 'idperfilconqueestaactivo', 'activarparaqueseveaenfront')
    list_editable = ('nivel_porcentaje', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront',)

# 10. HABILIDADES
@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre_habilidad', 'categoria', 'idperfilconqueestaactivo', 'activarparaqueseveaenfront')
    list_filter = ('categoria', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

# 11. CONFIGURACIÓN DE VISIBILIDAD (PANEL DE CONTROL DE ÍCONOS)
@admin.register(ConfiguracionVisible)
class ConfiguracionVisibleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_garage')
    list_editable = ('mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_garage')
    
    # Esto organiza mejor la vista dentro del registro
    fieldsets = (
        ('Panel de Control del Menú', {
            'description': 'Aquí puedes activar o desactivar los íconos visibles en la barra de navegación del CV.',
            'fields': ('mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_garage')
        }),
    )

    def has_add_permission(self, request):
        # Si ya existe 1 configuración, no dejar crear otra.
        # Solo queremos un panel de control único.
        return False if self.model.objects.count() > 0 else True

    def has_delete_permission(self, request, obj=None):
        # Evitar borrar la configuración por error
        return False
