from django.contrib import admin
from django.urls import path, re_path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth.models import User

urlpatterns = [
    # RUTAS ADMINISTRATIVAS
    path('admin/', admin.site.urls),
    
    # RUTAS DE AUTENTICACIÓN
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
    # RUTAS DE APLICACIÓN
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.tasks, name='tasks'),

    # CORRECCIÓN AQUÍ: Antes decía views.home, ahora dice views.garage_store
    path('perfil/<str:username>/garage/', views.garage_store, name='garage_store'), 

    # RUTAS DE PERFIL Y PDF
    path('perfil/<str:username>/', views.profile_cv, name='profile_cv'),
    path('perfil/<str:username>/pdf/', views.export_pdf, name='export_pdf'),
    
    # SERVIR ARCHIVOS MEDIA EN PRODUCCIÓN (RENDER)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)