from django.shortcuts import render
from .models import *
from django.db.models import Q,Prefetch

# Create your views here.
# URL de la pagina de inicio (esta no cuenta).
def inicio (request):
    return render(request, 'inicio.html')

#URL que muestra todos los Tutoriales
def listar_tutoriales (request):
    tutorial = Tutorial.objects.select_related("usuario").prefetch_related(
        Prefetch('categoria_del_tutorial'),
        Prefetch('Etiquetas_del_tutorial'),
        Prefetch('Tutoriales_cursos')
    ).order_by('fecha_Creacion').all()
    return render(request, 'Tutorial/listaTutorial.html', {"tutoriales_mostrar": tutorial})

#URL que muestra todos los Usuarios
def listar_usuarios (request):
    usuario = Usuario.objects.select_related(
        "perfiles_Usuarios",
        "Certificado_Usuarios"
    ).prefetch_related(
        Prefetch("usuario_del_tutorial"),
        Prefetch("Favoritos_del_usuario"),
        Prefetch("usuarios_del_curso"),
    ).all()
    return render(request, 'Usuario/listaUsuario.html', {"usuaios_mostrar": usuario})

#URL que muestra todos los usuarios con certificados de los cursos
