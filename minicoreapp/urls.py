from django.urls import path
from . import views

urlpatterns = [
    path('', views.filtrar_ventas, name='filtro_ventas'),
    path('magia/', views.inyectar_datos, name='inyectar_datos'), # <--- NUESTRA RUTA SECRETA
]