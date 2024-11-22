from django.shortcuts import render
from .models import *
from django.db.models import Q,Prefetch,Sum
from django.views.defaults import page_not_found
from .forms import *


# Create your views here.
# URL de la pagina de inicio (esta no cuenta).
def inicio (request):
    return render(request, 'Padre.html')

#URL que muestra todos los Tutoriales
#Requisitos: filtro Limit.
def listar_tutoriales (request):
    tutorial = Tutorial.objects.select_related("usuario").prefetch_related(
        Prefetch('categoria_del_tutorial'),
        Prefetch('Etiquetas_del_tutorial'),
        Prefetch('Tutoriales_cursos')
    ).order_by('fecha_Creacion').all()[:3]
    return render(request, 'Tutorial/listaTutorial.html', {"tutoriales_mostrar": tutorial})

#URL que muestra todos los Usuarios y sus datos relacionados
#Requisitos: Relacion reversa atraves de los related_name
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
#Requisitos: Parametro entero

def muestra_certificado_usuario_igual_id (request, id_usuario):
    certificado = Certificado.objects.select_related(
        "usuario",
        "curso"
    ).filter(usuario__id=id_usuario).first()
    #EL METODO FIRST ES UN METODO EL CUAL TE DEVUELVE EL PRIMER OBJETO QUE OBTENGA DE LA QUERY Y LAS PROPIEDADES QUE TENGAS EN EL HTML
    return render(request, 'Certificado/muestra_certificado_igual_idUser.html', {"certificado_mostrar": certificado})

#URL que dando una palaba te muestre los comentarios de todos los cursos que contienen esa palabra
#Requisitos: Parametro String

def muestra_comentario_equals_palabra (request, palabra):
    comentario = Comentario.objects.select_related("usuario").filter(contenido__contains = palabra).all()
    return render(request, 'Comentario/comentarios_equals_palabra.html', {'comentario_mostrar': comentario})

#URL que dado una palabra que sea una etiqueta con unos requisitos (expresion regular) nos devuelva el tutorial que tiene esa etiqueta
#Requisistos: re_path

def muestra_tutorial_por_etiqueta (request, etiquetas):
    tutorial = Tutorial.objects.select_related("usuario").prefetch_related(
        Prefetch('categoria_del_tutorial'),
        Prefetch('Etiquetas_del_tutorial'),
        Prefetch('Tutoriales_cursos')
    ).filter(Etiquetas_del_tutorial__nombre__contains = etiquetas).all()
    return render(request, 'Tutorial/muestra_tutorial_por_etiqueta.html', {"tutoriales_mostrar": tutorial})

#URL que muestra a los usuarios y la informafion de ellos nacidos entre dos años comprendidos
#Requisitos: 2 paramteros, filtro AND

def lista_usuarios_entre_años (request, año1, año2):
    usuario = Usuario.objects.select_related(
        "perfiles_Usuarios",
        "Certificado_Usuarios"
    ).prefetch_related(
        Prefetch("usuario_del_tutorial"),
        Prefetch("Favoritos_del_usuario"),
        Prefetch("usuarios_del_curso"),
    ).filter(
        Q(perfiles_Usuarios__fecha_Nacimiento__year__gte = año1) & Q(perfiles_Usuarios__fecha_Nacimiento__year__lte = año2)
    ).all()
    return render(request, 'Usuario/lista_usuarios_entre_años.html', {"usuaios_mostrar": usuario})

#URL que dada una categoria, te muestre todos los tutoriales que tienen esa categoria.
#Requisitos: filtro OR.

def lista_tutorial_por_categoria (request, categoria1, categoria2):
    tutorial = Tutorial.objects.select_related("usuario").prefetch_related(
        Prefetch('categoria_del_tutorial'),
        Prefetch('Etiquetas_del_tutorial'),
        Prefetch('Tutoriales_cursos')
    ).filter(Q(categoria_del_tutorial__nombre__contains = categoria1) | Q(categoria_del_tutorial__nombre__contains = categoria2)).all()
    return render(request, 'Tutorial/lista_tutorial_por_categoria.html', {"tutoriales_mostrar": tutorial})

#URl que muestra el total de todas las visitas de los tutoriales
#Requisitos: filtro agregate

def total_visitas (request):
    tutorial = Tutorial.objects.select_related("usuario").prefetch_related(
        Prefetch('categoria_del_tutorial'),
        Prefetch('Etiquetas_del_tutorial'),
        Prefetch('Tutoriales_cursos')
    )
    total_visitas = tutorial.aggregate(total_visitas=Sum('visitas'))
    return render(request, 'Tutorial/total_visitas.html', {"tutoriales_mostrar": tutorial, "total_visitas": total_visitas['total_visitas']})

#URL que muestra los tutoriales que no tengan visitas
#Requisitos: filtro None

def tutorial_no_tenga_categoria (request):
    tutorial = Tutorial.objects.select_related("usuario").prefetch_related(
        Prefetch('categoria_del_tutorial'),
        Prefetch('Etiquetas_del_tutorial'),
        Prefetch('Tutoriales_cursos')
    ).filter(categoria_del_tutorial = None).all()
    return render(request, 'Tutorial/tutorial_no_tenga_categoria.html', {"tutoriales_mostrar": tutorial})

#URL que muestra las subcategorias

def lista_subcategoria(request):
    subcategoria = SubCategoria.objects.select_related('categoria').all()
    return render(request, 'Subcategoria/lista_subcategoria.html', {"subcategoria_mostrar": subcategoria})

#URL que muestra el error 400

def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

#URL que muestra el error 403

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

#URL que muestra el error 404

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#URL que muestra el error 500
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)

###################################################################################################

#TEMPLATES DE LOS FORMUALRIOS

def usuario_Form (request):
    formulario = UsuarioForm()
    return render(request, 'formulario/usuarioFormulario.html', {'formulario': formulario})
    