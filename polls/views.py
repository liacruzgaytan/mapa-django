from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Pregunta, Opcion
from .forms import FormularioPregunta, FormularioOpciones

def inicio(request):
    # Página inicial con botones: encuestas, mapa, crear encuesta, descargas
    return render(request, 'polls/inicio.html')

def listado_preguntas(request):
    preguntas_recientes = Pregunta.objects.order_by('-fecha_publicacion')[:5]
    contexto = {'preguntas_recientes': preguntas_recientes}
    return render(request, 'polls/index.html', contexto)

def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'polls/detail.html', {'pregunta': pregunta})

def resultados(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'polls/results.html', {'pregunta': pregunta})

# vista resultados
def resultados_generales(request):
    preguntas = Pregunta.objects.all()
    return render(request, 'polls/resultados_generales.html', {'preguntas': preguntas})


@require_POST
def votar(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        opcion_seleccionada = pregunta.opcion_set.get(pk=request.POST['opcion'])
    except (KeyError, Opcion.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'pregunta': pregunta,
            'mensaje_error': "No seleccionaste una opción.",
        })
    else:
        opcion_seleccionada.votos += 1
        opcion_seleccionada.save()
        return HttpResponseRedirect(reverse('polls:resultados', args=(pregunta.id,)))

def mapa(request):
    return render(request, 'polls/mapa.html')

def crear_encuesta(request):
    mensaje_error = None

    if request.method == 'POST':
        formulario = FormularioPregunta(request.POST)
        formulario_opciones = FormularioOpciones(request.POST)

        if formulario.is_valid() and formulario_opciones.is_valid():
            opciones = formulario_opciones.save(commit=False)

            # Validar que al menos una opción tenga texto
            opciones_validas = [op for op in opciones if op.texto_opcion.strip()]
            if not opciones_validas:
                mensaje_error = "⚠️ Debes ingresar al menos una opción de respuesta."
            else:
                pregunta = formulario.save(commit=False)
                pregunta.fecha_publicacion = timezone.now()
                pregunta.save()
                for opcion in opciones_validas:
                    opcion.pregunta = pregunta
                    opcion.save()
                return redirect('polls:listado_preguntas')
        else:
            mensaje_error = "⚠️ La encuesta no se pudo guardar. Verifica que todos los campos estén completos y sean válidos."
    else:
        formulario = FormularioPregunta()
        formulario_opciones = FormularioOpciones()

    return render(request, 'polls/crear_encuesta.html', {
        'formulario': formulario,
        'formulario_opciones': formulario_opciones,
        'mensaje_error': mensaje_error
    })

def descargas(request):
    archivos = [
        {'nombre': 'Plantilla base.xlsx', 'ruta': 'Plantilla_base.xlsx'},
        {'nombre': 'Manual.pdf', 'ruta': 'Manual.pdf'},
    ]
    return render(request, 'polls/descargas.html', {'archivos': archivos})

#Editar preguntas y opciones
def editar_encuesta(request, pk):
    pregunta = get_object_or_404(Pregunta, pk=pk)
    form_pregunta = FormularioPregunta(request.POST or None, instance=pregunta)
    form_opciones = FormularioOpciones(request.POST or None, instance=pregunta)

    if form_pregunta.is_valid() and form_opciones.is_valid():
        form_pregunta.save()
        form_opciones.save()
        return redirect('polls:resultados_generales')

    return render(request, 'polls/editar_encuesta.html', {
        'form_pregunta': form_pregunta,
        'form_opciones': form_opciones
    })