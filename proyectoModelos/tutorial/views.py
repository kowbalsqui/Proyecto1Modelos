from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .models import *
from django.db.models import Sum
from .forms import *
from django.contrib import messages


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

#VISTAS DE LOS FORMUALRIOS

def usuario_Form(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            try:
                # Guarda el usuario en la base de datos
                formulario.save()
                return redirect('listar_ususario')
            except Exception as error:
                print(error)
    else:
        formulario = UsuarioForm()
        
    return render(request, 'formulario/usuarioFormulario.html', {"formulario": formulario})


def perfil_Form(request):
    if request.method == 'POST':
        formulario = PerfilForm(request.POST)
        if formulario.is_valid():
            try:
                # Guarda el perfil del usuario en la base de datos
                formulario.save()
                return redirect('listar_ususario')
            except Exception as error:
                print(error)
    else:
        formulario = PerfilForm()
        
    # Devuelve el formulario con los datos ingresados o el formulario vacío en caso de GET
    return render(request, 'formulario/perfilFormulario.html', {"formulario": formulario})

def tutorial_Form(request):
    if request.method == 'POST':
        formulario = TutorialForm(request.POST)
        if formulario.is_valid():
            try:
                #Guarda el tutorial en la base de datos
                formulario.save()
                return redirect('listar_tutoriales')
            except Exception as error: 
                print(error)
    else: 
        formulario = TutorialForm()
        
    #Devuele el formulario con los datos ingresados o el formulario vacio en caso de GET
    return render(request, 'formulario/tutorialFormulario.html', {"formulario":formulario})

def subcategoria_Form(request):
    if request.method == 'POST':
        formulario = SubcategoriaForm(request.POST)
        if formulario.is_valid():
            try:
                #Guarda el formulario en la basde de datos
                formulario.save()
                return redirect('lista_subcategoria')
            except Exception as error: 
                print(error)
    else:
        formulario = SubcategoriaForm()
        
        #Devuelve el formulario con los datos ingresados o el formulario vacío en caso de GET
        return render (request, 'formulario/subcategoriaFormulario.html', {"formulario": formulario})
        
def comentario_Form(request):
    if request.method == 'POST':
        formulario = ComentarioForm(request.POST)
        if formulario.is_valid():
            try:
                #Guarda el comentario en la base de datos
                formulario.save()
                return redirect('muestra_comentario_equals_palabra')
            except Exception as error: 
                print(error)
    else:
        formulario = ComentarioForm()
        
        #Devuelve el formulario con los datos ingresados o el formulario vacio en caso de GET
        return render(request, 'formulario/comentarioFomulario.html', {"formulario":formulario})   
    
def certificado_Form(request):
    if request.method == 'POST':
        formulario = CertificadoForm(request.POST)
        if formulario.is_valid():
            try:
                # Guarda el certificado en la base de datos
                formulario.save()
                return redirect('muestra_certificado_usuario_mismo_id')  # Reemplaza con la URL correcta
            except Exception as error:
                print(error)
                # Aquí puedes manejar el error de una manera más adecuada
    else:
        formulario = CertificadoForm()  # Formulario vacío para GET

    # Devuelve el formulario con los datos ingresados o el formulario vacío
    return render(request, 'formulario/certificadoFormulario.html', {'formulario': formulario}) 

def busqueda_avanzada(request):
    query = request.GET.get('query', '')  # Recupera el término de búsqueda
    tipo_busqueda = request.GET.get('tipo_busqueda', 'usuario')  # Recupera el tipo de búsqueda (usuario o curso)

    usuarios = []
    cursos = []
    tutorial = []
    comentario = []

    if query:
        if tipo_busqueda == 'usuario':
            usuarios = Usuario.objects.filter(nombre__icontains=query)
        elif tipo_busqueda == 'curso':
            cursos = Curso.objects.filter(nombre__icontains=query)
        elif tipo_busqueda == 'tutorial':
            tutorial = Tutorial.objects.filter(titulo__icontains=query)
        elif tipo_busqueda == 'comentario':
            comentario = Comentario.objects.filter(contenido__icontains=query)
    
    # Devuelve los resultados a un template dentro de la carpeta 'formulario'
    return render(request, 'formulario/busqueda_resultado.html', {
        'usuarios': usuarios,
        'cursos': cursos,
        'tutorial': tutorial,
        'comentario':comentario,
    })

def filtros_avanzados(request):
    formulario = BusquedaAvanzadaUsuario(request.GET or None)
    usuarios = Usuario.objects.all()

    if request.GET:  # Si hay datos enviados por GET
        if formulario.is_valid():
            puntuacion = formulario.cleaned_data.get('puntuacion')
            activo = formulario.cleaned_data.get('es_activo')
            fecha_Registro = formulario.cleaned_data.get('fecha_Registro')

            # Aplicamos los filtros
            if puntuacion is not None:
                usuarios = usuarios.filter(puntuacion=puntuacion)
            if activo:
                usuarios = usuarios.filter(es_activo = True)
            if fecha_Registro:
                usuarios = usuarios.filter(fecha_Registro__gte=fecha_Registro)
        else:
            # Si el formulario no es válido, mostramos los errores
            return render(request, 'MenuNavegacion.html', {
                'formulario': formulario,
                'usuarios': [],
            })

    # Siempre renderiza un HttpResponse
    return render(request, 'formulario/busqueda_avanzada_user.html', {
        'formulario': formulario,
        'usuarios': usuarios,
    })



def filtros_avanzados_tutoriales(request):
    # Inicializamos el queryset
    tutoriales = Tutorial.objects.all()

    # Capturamos los valores de los filtros
    titulo = request.GET.get('titulo')
    fecha_creacion = request.GET.get('fecha_Creacion')
    valoracion = request.GET.get('valoracion')

    # Filtros avanzados
    if titulo:
        tutoriales = tutoriales.filter(titulo__icontains=titulo)  # Título contiene la palabra clave
    if fecha_creacion:
        tutoriales = tutoriales.filter(fecha_Creacion__gte=fecha_creacion)  # Fecha de creación mayor o igual
    if valoracion:
        tutoriales = tutoriales.filter(valoracion__gte=valoracion)  # Valoración mínima

    # Renderizamos la plantilla
    return render(request, 'formulario/filtros_avanzados_tutoriales.html', {'tutoriales': tutoriales})

def filtros_avanzados_perfil(request):
    perfiles = Perfil.objects.all()
    
    fecha_nacimiento = request.GET.get('fecha_Nacimiento')
    redes = request.GET.get('redes')
    estudios = request.GET.get('estudios')
    
    if fecha_nacimiento:
        perfiles = perfiles.filter(fecha_Nacimiento__gte=fecha_nacimiento)  # Fecha de nacimiento mayor o igual
    if redes:
        perfiles = perfiles.filter(redes = redes)
    if estudios:
        perfiles = perfiles.filter(estudios__icontains = estudios)
        
    return render(request, 'formulario/filtros_avanzados_perfiles.html', {'perfiles': perfiles})

def pagina_de_enlaces(request):
    return render(request, 'enlaces.html')
