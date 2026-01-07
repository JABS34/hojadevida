from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    # PANEL DE ADMINISTRACIÓN DE DJANGO
    path('admin/', admin.site.urls),

    # --- SECCIONES PRINCIPALES ---
    # 1. Pantalla de Bienvenida (Landing Page)
    path('', views.home, name='home'),
    
    # 2. Tu Panel de Edición Personal (Donde ingresas tu info)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # 3. Tu CV Público Interactivo con Diseño 3D
    path('perfil/<str:username>/', views.profile_cv, name='profile_cv'),

    # --- AUTENTICACIÓN ---
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),

    # --- SISTEMA DE TAREAS (OPCIONAL) ---
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]