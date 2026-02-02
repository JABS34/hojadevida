from django.contrib import admin
from django.urls import path, re_path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth.models import User

# FUNCIÓN TEMPORAL PARA CREAR TU USUARIO
def crear_mi_usuario(request):
    from django.http import HttpResponse
    if not User.objects.filter(username='jabs6393').exists():
        User.objects.create_superuser('jabs6393', 'admin@ejemplo.com', 'jabs12345')
        return HttpResponse("Usuario creado con éxito. Ya puedes borrar este código.")
    return HttpResponse("El usuario ya existe.")

urlpatterns = [
    # RUTAS ADMINISTRATIVAS
    path('crear-admin-secreto/', crear_mi_usuario),
    path('admin/', admin.site.urls),
    
    # RUTAS DE AUTENTICACIÓN
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
    # RUTAS DE APLICACIÓN
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.tasks, name='tasks'),

    # ESTA ES LA RUTA QUE FALTABA Y CAUSABA EL ERROR
    path('perfil/<str:username>/garage/', views.home, name='garage_store'), 

    # RUTAS DE PERFIL Y PDF
    path('perfil/<str:username>/', views.profile_cv, name='profile_cv'),
    path('perfil/<str:username>/pdf/', views.export_pdf, name='export_pdf'),
    
    # SERVIR ARCHIVOS MEDIA EN PRODUCCIÓN (RENDER)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# SERVIR ARCHIVOS MEDIA EN DESARROLLO (LOCAL)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)