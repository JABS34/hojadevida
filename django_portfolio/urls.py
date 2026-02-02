from django.contrib import admin
from django.urls import path, re_path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth.models import User # Importamos el modelo de usuario

# FUNCIÓN TEMPORAL PARA CREAR TU USUARIO
def crear_mi_usuario(request):
    from django.http import HttpResponse
    if not User.objects.filter(username='jabs6393').exists():
        User.objects.create_superuser('jabs6393', 'admin@ejemplo.com', 'jabs12345')
        return HttpResponse("Usuario creado con éxito. Ya puedes borrar este código.")
    return HttpResponse("El usuario ya existe.")

urlpatterns = [
    # RUTA SECRETA PARA CREAR AL ADMIN (Úsala una sola vez)
    path('crear-admin-secreto/', crear_mi_usuario),

    # RUTAS DEL SISTEMA (ADMIN PRIMERO)
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.tasks, name='tasks'),

    # PERFILES AL FINAL
    path('perfil/<str:username>/', views.profile_cv, name='profile_cv'),
    path('perfil/<str:username>/pdf/', views.export_pdf, name='export_pdf'),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
