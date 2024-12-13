from django.shortcuts import render,redirect,  get_object_or_404
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

#CREAR

def usuario_Form(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST, request.FILES)
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
                return redirect('filtros_avanzados_perfil')
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

def pagina_de_enlaces(request):
    return render(request, 'enlaces.html')


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

#BUSQUEDA AVANZADA

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
    formulario = BusquedaAvanzadaUsuario(request.GET, request.FILES)

    if len(request.GET) > 0:
        if request.GET:  # Si hay datos enviados por GET
            if formulario.is_valid():
                usuarios = Usuario.objects
                
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
                
                usuarios = usuarios.all()
            else:
                # Si el formulario no es válido, mostramos los errores
                return render(request, 'MenuNavegacion.html', {
                    'formulario': formulario,
                    'usuarios': [],
                })
    else:
    # Siempre renderiza un HttpResponse
        usuarios = Usuario.objects.all()
        return render(request, 'formulario/busqueda_avanzada_user.html', {
            'formulario': formulario,
            'usuarios': usuarios,
        })



def filtros_avanzados_tutoriales(request):
    formulario = BusquedaAvanzadaTutorial(request.GET)  # Inicializa el formulario
    tutoriales = Tutorial.objects.all().select_related('usuario')  # Inicializa los tutoriales
    usuarios = Usuario.objects.all()  # Obtén todos los usuarios

    if len(request.GET) > 0:
        if request.GET:  # Si hay parámetros en el GET
            if formulario.is_valid():
                # Obtén los datos del formulario
                visitas = formulario.cleaned_data.get('visitas')
                valoracion = formulario.cleaned_data.get('valoracion')
                usuario = formulario.cleaned_data.get('usuario')

                # Aplica los filtros solo si los valores están presentes
                if visitas:
                    tutoriales = tutoriales.filter(visitas=visitas)
                if valoracion:
                    tutoriales = tutoriales.filter(valoracion=valoracion)
                if usuario:
                    tutoriales = tutoriales.filter(usuario=usuario)
            else:
                # Si el formulario no es válido, se queda en la misma página
                return render(request, 'formulario/filtros_avanzados_tutoriales.html', {
                    'formulario': formulario,
                    'tutoriales': [],
                    'usuarios': usuarios,
                })

    # Renderiza la plantilla con los resultados (o todos los tutoriales si no hay filtros)
    return render(request, 'formulario/filtros_avanzados_tutoriales.html', {
        'formulario': formulario,
        'tutoriales': tutoriales,
        'usuarios': usuarios,
    })


def filtros_avanzados_perfil(request):
    formulario = BusquedaAvanzadaPerfil(request.GET)

    if len(request.GET) > 0:
        if request.GET:
            perfiles = Perfil.objects
            if formulario.is_valid():
                fecha_Nacimiento = formulario.cleaned_data.get('fecha_Nacimiento')
                redes = formulario.cleaned_data.get('redes')
                estudios = formulario.cleaned_data.get('estudios')

                if fecha_Nacimiento:
                    perfiles = perfiles.filter(fecha_Nacimiento__gte=fecha_Nacimiento)

                if redes:
                    perfiles = perfiles.filter(redes=redes)

                if estudios:
                    perfiles = perfiles.filter(estudios__icontains=estudios)
                
                perfiles = perfiles.all()

            else:
                return render(request, 'formulario/filtros_avanzados_perfiles.html', {
                    'formulario': formulario,
                    'perfiles': []
                })
    else:
        perfiles = Perfil.objects.all()  # Obtener todos los perfiles si no hay filtros

        return render(request, 'formulario/filtros_avanzados_perfiles.html', {
            'formulario': formulario,
            'perfiles': perfiles
        })

def filtrosAvanzadosSubcategorias(request):
    formulario = BusquedaAvanzadaSubcategorias(request.GET)

    if len(request.GET) > 0:
        if request.GET:
            subcategorias = SubCategoria.objects
            categoria = Categoria.objects
            if formulario.is_valid():
                nombre = formulario.cleaned_data.get('nombre')
                activa = formulario.cleaned_data.get('activa')
                categoria = formulario.cleaned_data.get('categoria')

                # Aplicar filtros según los valores del formulario
                if nombre:
                    subcategorias = subcategorias.filter(nombre__icontains=nombre)

                if activa:
                    subcategorias = subcategorias.filter(activa=True)

                if categoria:
                    subcategorias = subcategorias.filter(categoria=categoria)
                
                subcategorias = subcategorias.all()
                categoria = categoria.all()
            else:
                # Si el formulario no es válido, mostrar errores
                return render(request, 'formulario/filtros_avanzados_subcategorias.html', {
                    'formulario': formulario,
                    'subcategorias': [],
                    'categoria':categoria
                })
    else:
        subcategorias = SubCategoria.objects.all()
        categoria = Categoria.objects.all()
        # Renderizar resultados filtrados o todos si no hay filtros
        return render(request, 'formulario/filtros_avanzados_subcategorias.html', {
            'formulario': formulario,
            'subcategorias': subcategorias,
            'categoria':categoria
        })

def filtrosAvanzadosComentarios(request):
    formulario = BusquedaAvanzadaComentarios(request.GET)

    if len(request.GET) > 0:
        if request.GET:
            comentarios = Comentario.objects
            if formulario.is_valid():
                contenido = formulario.cleaned_data.get('contenido')
                visible = formulario.cleaned_data.get('visible')
                puntuacion = formulario.cleaned_data.get('puntuacion')

                if contenido:
                    comentarios = comentarios.filter(contenido__icontains=contenido)
                
                if visible:
                    comentarios = comentarios.filter(visible=True)

                if puntuacion:
                    comentarios = comentarios.filter(puntuacion= puntuacion)
                    
                comentarios = comentarios.all()
            else:
                return render (request, 'formulario/filtros_avanzados_comentarios.html', {
                    'formulario': formulario,
                    'comentarios': []
                })
    else:
        comentarios = Comentario.objects.all()
        return render (request, 'formulario/filtros_avanzados_comentarios.html', {
            'formulario': formulario,
            'comentarios': comentarios
        })

def filtrosAvanzadosCertificados (request):
    formulario = BusquedaAvanzadaCertificados(request.GET)   

    if len(request.GET) > 0:
        if request.GET:
            certificados = Certificado.objects
            if formulario.is_valid():
                codigo_verificacion = formulario.cleaned_data.get('codigo_verificacion') 
                nivel = formulario.cleaned_data.get('nivel')
                fecha_emision = formulario.cleaned_data.get('fecha_emision')

            if codigo_verificacion:
                certificados = certificados.filter(codigo_verificacion__icontains= codigo_verificacion)
            
            if nivel: 
                certificados = certificados.filter(nivel= nivel)
                
            if fecha_emision:
                certificados = certificados.filter(fecha_emision= fecha_emision)
            
            certificados = certificados.all() 
        else:
                return render (request, 'formulario/filtros_avanazados_certificados.html', {
                    'formulario':formulario,
                    'certificados':[]
                })
    else:
        certificados = Certificado.objects.all()
        return render (request, 'formulario/filtros_avanazados_certificados.html', {
            'formulario':formulario,
            'certificados': certificados
        })

#MODIFICAR

def usuario_modificar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)  # Obtenemos el usuario a modificar

    if request.method == 'POST':
        # Incluimos request.FILES para manejar archivos
        formulario = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()  # Guardamos el usuario con los datos modificados
            messages.success(request, "Usuario modificado correctamente")
            return redirect('filtros_avanzados')  # Redirige a una vista que muestre los usuarios
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        formulario = UsuarioForm(instance=usuario)  # Cargamos el formulario con datos existentes

    return render(request, 'formulario/usuario_modificar.html', {
        'formulario': formulario,
        'usuario': usuario
    })


# def usuario_modificar(request,usuario_id):
#     usuario = Usuario.objects.get(id=usuario_id)

#     datosFormulario = None

#     if request.method == "POST":
#         datosFormulario = request.POST


#     formulario = UsuarioForm(datosFormulario,instance = usuario)

#     if (request.method == "POST"):

#         if formulario.is_valid():
#             try:
#                 formulario.save()
#                 messages.success(request, 'Se ha editado el Usuario '+formulario.cleaned_data.get('nombre')+" correctamente")
#                 return redirect('filtros_avanzados')
#             except Exception as error:
#                 print(error)
#     return render(request, 'formulario/usuario_modificar.html',{"formulario":formulario,"usuario":usuario})

def tutorial_modificar(request, tutorial_id):
    tutorial = Tutorial.objects.get(id= tutorial_id)

    datosFormulario = None

    if request.method == 'POST':
        datosFormulario = request.POST

    formulario = TutorialForm(datosFormulario, instance= tutorial)

    if (request.method == 'POST'):

        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado el Tutorial correctamente')
                return redirect('filtros_avanzados_tutoriales')
            except Exception as error:
                print(error)
    return render(request, 'formulario/tutorial_modificar.html',{"formulario":formulario,"tutorial":tutorial})

def perfil_modificar(request, perfil_id):
    perfil = Perfil.objects.get(id= perfil_id)

    datosFormulario = None

    if request.method == 'POST':
        datosFormulario = request.POST

    formulario = PerfilForm(datosFormulario, instance= perfil)

    if (request.method == 'POST'):

        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado el Perfil correctamente')
                return redirect('filtros_avanzados_perfil')
            except Exception as error:
                print(error)
    return render(request, 'formulario/perfil_modificar.html',{"formulario":formulario,"perfil":perfil})

def subcategoria_modificar(request, subcategoria_id):
    subcategoria = SubCategoria.objects.get(id= subcategoria_id)

    datosFormulario = None

    if request.method == 'POST':
        datosFormulario = request.POST

    formulario = SubcategoriaForm(datosFormulario, instance= subcategoria)

    if (request.method == 'POST'):

        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado la subcategoria correctamente')
                return redirect('filtros_avanzados_subcategorias')
            except Exception as error:
                print(error)
    return render(request, 'formulario/subcategoria_modificar.html',{"formulario":formulario,"subcategoria":subcategoria})

def comentario_modificar(request, comentario_id):
    comentario = Comentario.objects.get(id= comentario_id)

    datosFormulario = None

    if request.method == 'POST':
        datosFormulario = request.POST

    formulario = ComentarioForm(datosFormulario, instance= comentario)

    if (request.method == 'POST'):

        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado el comentario correctamente')
                return redirect('filtros_avanzados_comentarios')
            except Exception as error:
                print(error)
    return render(request, 'formulario/comentario_modificar.html',{"formulario":formulario,"comentario":comentario})

def certificado_modificar(request, certificado_id):
    certificado = Certificado.objects.get(id= certificado_id)

    datosFormulario = None

    if request.method == 'POST':
        datosFormulario = request.POST

    formulario = CertificadoForm(datosFormulario, instance= certificado)

    if (request.method == 'POST'):

        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado el certificado correctamente')
                return redirect('filtros_avanzados_certificados')
            except Exception as error:
                print(error)
    return render(request, 'formulario/certificado_modificar.html',{"formulario":formulario,"certificado":certificado})

#ELIMINAR

def eliminar_usuario(request,usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    try:
        usuario.delete()
        messages.success(request, "Se ha elimnado el usuario "+usuario.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('filtros_avanzados')


def eliminar_tutorial(request,tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    try:
        tutorial.delete()
        messages.success(request, "Se ha elimnado el Tutorial correctamente")
    except Exception as error:
        print(error)
    return redirect('filtros_avanzados_tutoriales')



def eliminar_perfil(request,perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    try:
        perfil.delete()
        messages.success(request, "Se ha elimnado el Perfil correctamente")
    except Exception as error:
        print(error)
    return redirect('filtros_avanzados_perfil')


def eliminar_subcategoria(request,subcategoria_id):
    subcategoria = SubCategoria.objects.get(id=subcategoria_id)
    try:
        subcategoria.delete()
        messages.success(request, "Se ha elimnado la SuubCategoria correctamente")
    except Exception as error:
        print(error)
    return redirect('filtros_avanzados_subcategorias')

def eliminar_comentario(request,comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    try:
        comentario.delete()
        messages.success(request, "Se ha elimnado el Comentario correctamente")
    except Exception as error:
        print(error)
    return redirect('filtros_avanzados_comentarios')


def eliminar_certificado(request,certificado_id):
    certificado = Certificado.objects.get(id=certificado_id)
    try:
        certificado.delete()
        messages.success(request, "Se ha elimnado el Certificado correctamente")
    except Exception as error:
        print(error)
    return redirect('filtros_avanzados_certificados')
