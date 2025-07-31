from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.inicio, name="inicio"),                     # Página de inicio
    path("polls/", views.index, name="index"),                 # Lista de preguntas
    path("mapa/", views.mapa, name="mapa"),                    # Página del mapa
    path("crear/", views.crear_encuesta, name="crear_encuesta"),  # Crear nueva encuesta
    path("<int:question_id>/", views.detail, name="detail"),   # Detalle de pregunta
    path("<int:question_id>/results/", views.results, name="results"), # Resultados
    path("<int:question_id>/vote/", views.vote, name="vote"),         # Votación
 path('favicon.ico', lambda request: HttpResponse(status=204)),
]
