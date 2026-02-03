from django.contrib import admin
from django.urls import path, re_path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # RUTAS ADMINISTRATIVAS
    path('admin/', admin.site.urls),
    
    # RUTAS DE AUTENTICACIÓN Y BIENVENIDA
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
    # RUTAS DE APLICACIÓN (Dashboard y Tareas)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.tasks, name='tasks'),

    # RUTA DEL GARAGE (Venta de productos)
    path('perfil/<str:username>/garage/', views.garage_store, name='garage_store'), 

    # RUTA DEL PERFIL CV PUBLICO
    path('perfil/<str:username>/', views.profile_cv, name='profile_cv'),
    
    # RUTA PARA EXPORTAR PDF
    path('perfil/<str:username>/pdf/', views.export_pdf, name='export_pdf'),
    
    # SERVIR ARCHIVOS MEDIA EN PRODUCCIÓN (Render)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)