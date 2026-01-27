from django.contrib import admin
from django.urls import path, include
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve # Necesario para forzar la visualización en Render
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/<str:username>/', views.profile_cv, name='profile_cv'),
    
    # NUEVA RUTA: Venta de Garage (Ya la tienes configurada correctamente)
    path('garage/', views.garage_store, name='garage_store'),
    
    # Autenticación
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
    # Tareas
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    
    # RUTA CRÍTICA: Esto sirve las fotos en Render aunque DEBUG sea False
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]

# También mantenemos la configuración estándar por si acaso para desarrollo local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
