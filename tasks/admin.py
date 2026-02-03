from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    CursosRealizados, Reconocimiento, VentaGarage,
    ProductosAcademicos, ProductosLaborales,
    LenguajeProgramacion, Habilidad, ConfiguracionVisible
)

# --- PERSONALIZACIÓN DEL ENCABEZADO DEL PANEL ---
admin.site.site_header = "Administración de Portafolio"
admin.site.site_title = "Panel de Control"
admin.site.index_title = "Gestión de Contenido Web"

# 1. TAREAS
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'important', 'created')
    list_filter = ('important', 'user')
    readonly_fields = ('created',)

# 2. DATOS PERSONALES
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'estado_visual')
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('nombres', 'apellidos', 'numerocedula')
    
    # Truco para mostrar un icono en vez de True/False
    def estado_visual(self, obj):
        return obj.activarparaqueseveaenfront
    estado_visual.boolean = True
    estado_visual.short_description = "Visible en Web"

# 3. EXPERIENCIA LABORAL
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'visible')
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    search_fields = ('cargodesempenado', 'nombrempresa')
    list_editable = ('activarparaqueseveaenfront',)
    
    def visible(self, obj):
        return obj.activarparaqueseveaenfront
    visible.boolean = True

# 4. RECONOCIMIENTOS
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'entidadpatrocinadora', 'visible')
    list_filter = ('tiporeconocimiento', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    
    def visible(self, obj):
        return obj.activarparaqueseveaenfront
    visible.boolean = True

# 5. CURSOS REALIZADOS
@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'entidadpatrocinadora', 'totalhoras', 'visible')
    search_fields = ('nombrerecurso', 'entidadpatrocinadora')
    list_editable = ('activarparaqueseveaenfront',)
    
    def visible(self, obj):
        return obj.activarparaqueseveaenfront
    visible.boolean = True

# 6. PRODUCTOS ACADÉMICOS
@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'visible')
    list_editable = ('activarparaqueseveaenfront',)
    
    def visible(self, obj):
        return obj.activarparaqueseveaenfront
    visible.boolean = True

# 7. PRODUCTOS LABORALES
@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'visible')
    list_filter = ('fechaproducto',)
    list_editable = ('activarparaqueseveaenfront',)
    
    def visible(self, obj):
        return obj.activarparaqueseveaenfront
    visible.boolean = True

# 8. VENTA GARAGE
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'precio_formato', 'estadoproducto', 'visible')
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront', 'estadoproducto')
    search_fields = ('nombreproducto',)
    
    def precio_formato(self, obj):
        return f"${obj.valordelbien}"
    precio_formato.short_description = "Precio"

    def visible(self, obj):
        return obj.activarparaqueseveaenfront
    visible.boolean = True

# 9. LENGUAJES DE PROGRAMACIÓN
@admin.register(LenguajeProgramacion)
class LenguajeProgramacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'barra_progreso', 'visible')
    list_editable = ('nivel_porcentaje', 'activarparaqueseveaenfront')
    
    # Muestra una barrita visual en el admin
    def barra_progreso(self, obj):
        return format_html(
            '<div style="width:100px; background:#ddd; border-radius:5px;">'
            '<div style="width:{}%; background:#28a745; height:10px; border-radius:5px;"></div>'
            '</div>',
            obj.nivel_porcentaje
        )
    barra_progreso.short_description = "Nivel"
    
    def visible(self, obj):
        return obj.activarparaqueseveaenfront
    visible.boolean = True

# 10. HABILIDADES
@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre_habilidad', 'categoria', 'visible')
    list_filter = ('categoria', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    
    def visible(self, obj):
        return obj.activarparaqueseveaenfront
    visible.boolean = True

# 11. CONFIGURACIÓN DE VISIBILIDAD
@admin.register(ConfiguracionVisible)
class ConfiguracionVisibleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_garage')
    list_editable = ('mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_garage')

    fieldsets = (
        ('Panel de Control del Menú', {
            'description': 'Activa o desactiva qué botones ve la gente en la página web.',
            'fields': (('mostrar_cursos', 'mostrar_reconocimientos', 'mostrar_garage'),)
        }),
    )

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True

    def has_delete_permission(self, request, obj=None):
        return False
