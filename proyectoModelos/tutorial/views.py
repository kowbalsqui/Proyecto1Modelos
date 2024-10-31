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

#URL que muestra todos los Usuarios y sus datos relacionados
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

#URL que muetra los certificados de un usuario el cual es un id que le entra a la query

def muestra_certificado_usuario_igual_id (request, id_usuario):
    certificado = Certificado.objects.select_related(
        "usuario",
        "curso"
    ).filter(usuario__id=id_usuario).first()
    #EL METODO FIRST ES UN METODO EL CUAL TE DEVUELVE EL PRIMER OBJETO QUE OBTENGA DE LA QUERY Y LAS PROPIEDADES QUE TENGAS EN EL HTML
    return render(request, 'Certificado/muestra_certificado_igual_idUser.html', {"certificado": certificado})

#URL que dando una palaba te muestre los comentarios de todos los cursos que contienen esa palabra

def muestra_comentario_equals_palabra (request, palabra):
    comentario = Comentario.objects.select_related("usuario").filter(contenido__contains = palabra).all()
    return render(request, 'Comentarios/comentarios_equals_palabra.html', {'comentario_mostrar': comentario})
