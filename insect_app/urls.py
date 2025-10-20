from django.urls import path
from . import views # Importa todas las vistas de tu_app/views.py
from django.contrib.auth import views as auth_views # Importa las vistas de autenticación de Django

urlpatterns = [
    # URLs de Autenticación
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # URLs para Temperatura
    path('temperaturas/', views.temperatura_list, name='temperatura_list'),
    path('temperaturas/crear/', views.temperatura_create, name='temperatura_create'),
    path('temperaturas/<int:pk>/actualizar/', views.temperatura_update, name='temperatura_update'),
    path('temperaturas/<int:pk>/eliminar/', views.temperatura_delete, name='temperatura_delete'),

    # URLs para Humedad
    path('humedades/', views.humedad_list, name='humedad_list'),
    path('humedades/crear/', views.humedad_create, name='humedad_create'),
    path('humedades/<int:pk>/actualizar/', views.humedad_update, name='humedad_update'),
    path('humedades/<int:pk>/eliminar/', views.humedad_delete, name='humedad_delete'),

    # URLs para Vida
    path('vidas/', views.vida_list, name='vida_list'),
    path('vidas/crear/', views.vida_create, name='vida_create'),
    path('vidas/<int:pk>/actualizar/', views.vida_update, name='vida_update'),
    path('vidas/<int:pk>/eliminar/', views.vida_delete, name='vida_delete'),

    # URLs para Mortalidad_pupas
    path('mortalidad-pupas/', views.mortalidad_pupas_list, name='mortalidad_pupas_list'),
    path('mortalidad-pupas/crear/', views.mortalidad_pupas_create, name='mortalidad_pupas_create'),
    path('mortalidad-pupas/<int:pk>/actualizar/', views.mortalidad_pupas_update, name='mortalidad_pupas_update'),
    path('mortalidad-pupas/<int:pk>/eliminar/', views.mortalidad_pupas_delete, name='mortalidad_pupas_delete'),

    path('temperatura-agua/', views.registrotemperaturaagua_list, name='registrotemperaturaagua_list'),
    path('temperatura-agua/crear/', views.registrotemperaturaagua_create, name='registrotemperaturaagua_create'),
    path('temperatura-agua/<int:pk>/actualizar/', views.registrotemperaturaagua_update, name='registrotemperaturaagua_update'),
    path('temperatura-agua/<int:pk>/eliminar/', views.registrotemperaturaagua_delete, name='registrotemperaturaagua_delete'),

    path('dashboard/', views.dashboard_view, name='dashboard'),

]