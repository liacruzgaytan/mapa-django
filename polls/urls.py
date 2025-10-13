from django.urls import path
from django.http import HttpResponse
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.inicio, name="inicio"),  # Página de inicio
    path("encuestas/", views.listado_preguntas, name="listado_preguntas"),  # Lista de preguntas
    path("mapa/", views.mapa, name="mapa"),  # Página del mapa
    path("crear/", views.crear_encuesta, name="crear_encuesta"),  # Crear nueva encuesta
    path("descargas/", views.descargas, name="descargas"),  # Descargas
    path("<int:pregunta_id>/", views.detalle, name="detalle"),  # Detalle de pregunta
    path("<int:pregunta_id>/resultados/", views.resultados, name="resultados"),  # Resultados
    path("<int:pregunta_id>/votar/", views.votar, name="votar"),  # Votación
    path("favicon.ico", lambda request: HttpResponse(status=204)), 
    path('resultados/', views.resultados_generales, name='resultados_generales'),
    path('encuesta/<int:pk>/editar/', views.editar_encuesta, name='editar_encuesta'),

]
