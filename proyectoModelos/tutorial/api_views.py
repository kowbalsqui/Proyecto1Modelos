from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from django.db.models import Q,Prefetch
from rest_framework import status
from rest_framework import viewsets
from django.core.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from oauth2_provider.models import AccessToken 
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

#Lista de tutoriales api

@api_view (['GET'])

def tutorial_list(request):
    tutorial = Tutorial.objects.all()
    serializer = TutorialSerializer(tutorial, many= True)
    return Response(serializer.data)

@api_view (['GET'])
def tutorial_list_simple(request):
    tutorial = Tutorial.objects.all()
    serializer = TutorialSerializerSimple(tutorial)
    return Response(serializer.data)

# Lista de usuario api

@api_view (['GET'])
def usuario_list(request):
    usuario = Usuario.objects.all()
    serializer = UsuarioSerializer(usuario, many = True)
    return Response(serializer.data)

@api_view (['GET'])
def cursos_list(request):
    cursos = Curso.objects.all().prefetch_related('usuario')
    serializers = CursosSerializer(cursos, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def comentario_list(request):
    comentario = Comentario.objects.all()
    serializers = ComentarioSerializers(comentario, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def comentario_list_simple(request):
    if not request.user.has_perm("tutorial.view_comentario"):
        raise PermissionDenied("❌ No tienes permiso para editar usuarios.")
    comentario = Comentario.objects.all()
    serializers = ComentarioSerializers(comentario, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def perfil_list(request):
    if not request.user.has_perm("tutorial.view_perfil"):
        raise PermissionDenied("❌ No tienes permiso para editar usuarios.")
    perfil = Perfil.objects.all()
    serializers = PerfilSerializers(perfil, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def perfil_list_simple(request):
    if not request.user.has_perm("tutorial.view_perfil"):
        raise PermissionDenied("❌ No tienes permiso para editar usuarios.")
    perfil = Perfil.objects.all()
    serializers = PerfilSerializersSimple(perfil, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def categoria_list(request):
    if not request.user.has_perm("tutorial.view_categroia"):
        raise PermissionDenied("❌ No tienes permiso para editar usuarios.")
    categoria = Categoria.objects.all()
    serializers = CategoriaSerializer(categoria, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def etiqueta_list(request):
    if not request.user.has_perm("tutorial.view_etiqueta"):
        raise PermissionDenied("❌ No tienes permiso para editar usuarios.")
    etiqueta = Etiqueta.objects.all()
    serializers = EtiquetaSerializer(etiqueta, many = True)
    return Response(serializers.data)

@api_view(['GET'])
def usuario_busqueda_simple(request):
    if not request.user.has_perm("tutorial.view_usuario"):
        raise PermissionDenied("❌ No tienes permiso para editar usuarios.")
    print("hello")
    form = BusquedaSimpleUsuario(request.query_params)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        usuarios = Usuario.objects.filter(Q(nombre__icontains=email) | Q(email__icontains=email))
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def listar_tutoriales_usuario(request):
    # Usa el filtro basado en la relación ForeignKey
    tutoriales = Tutorial.objects.filter(usuario=request.user)
    serializer = TutorialSerializer(tutoriales, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def obtenDatosUsuario (request):
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
def usuario_busqueda_avanzada(request):
    if not request.user.has_perm("tutorial.view_usuario"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)


    print("Datos recibidos en query_params:", request.query_params)  # Depuración
    
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaUsuario(request.query_params)
        
        if formulario.is_valid():
            QSusuarios = Usuario.objects.all()  # Inicia con todos los usuarios
            activo = formulario.cleaned_data.get('es_activo')
            puntuacion = formulario.cleaned_data.get('puntuacion')
            fecha_Registro = formulario.cleaned_data.get('fecha_Registro')
            
            if puntuacion is not None:
                if 1 <= puntuacion <= 5:
                    QSusuarios = QSusuarios.filter(puntuacion=puntuacion)
            
            if activo is not None:
                QSusuarios = QSusuarios.filter(es_activo=activo)
            
            if fecha_Registro:
                QSusuarios = QSusuarios.filter(fecha_Registro=fecha_Registro)
            
            usuarios = QSusuarios.all()
            serializer = UsuarioSerializer(usuarios, many=True)
            print("Usuarios encontrados:", serializer.data)  # Depuración
            return Response(serializer.data)
        else:
            print("Errores del formulario:", formulario.errors)  # Depuración
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "No se recibieron parámetros"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def tutorial_busqueda_avanzado(request):

    if not request.user.has_perm("tutorial.view_tutorial"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    print("Datos recibidos en query_params:", request.query_params)  # Depuración
    
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaTutorialApi(request.query_params)
        
        if formulario.is_valid():
            QSusuarios = Tutorial.objects.all()  # Inicia con todos los usuarios
            visitas = formulario.cleaned_data.get('visitas')
            valoracion = formulario.cleaned_data.get('valoracion')
            titulo = formulario.cleaned_data.get('titulo')  
            
            if visitas is not None and visitas > 0:
                QSusuarios = QSusuarios.filter(visitas=visitas)

            if valoracion is not None and valoracion > 0:
                QSusuarios = QSusuarios.filter(valoracion=valoracion)
            
            if titulo is not None:
                QSusuarios = QSusuarios.filter(titulo__icontains=titulo)
            
            usuarios = QSusuarios.all()
            serializer = TutorialSerializerSimple(usuarios, many=True)  
            print("Tutoriales encontrados:", serializer.data)  # Depuración
            return Response(serializer.data)
        else:
            print("Errores del formulario:", formulario.errors)  # Depuración
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "No se recibieron parámetros"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def perfil_busqueda_avanzada(request):

    if not request.user.has_perm("tutorial.view_perfil"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    print("Datos recibidos en query_params:", request.query_params)  # Depuración
    
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaPerfil(request.query_params)
        
        if formulario.is_valid():
            QSusuarios = Perfil.objects.all()  # Inicia con todos los usuarios
            fecha_Nacimiento = formulario.cleaned_data.get('fecha_Nacimiento')
            redes = formulario.cleaned_data.get('redes')
            estudios = formulario.cleaned_data.get('estudios')  
            
            if fecha_Nacimiento is not None:
                QSusuarios = QSusuarios.filter(fecha_Nacimiento=fecha_Nacimiento)

            if redes is not None:
                QSusuarios = QSusuarios.filter(redes=redes)
            
            if estudios is not None:
                QSusuarios = QSusuarios.filter(estudios__icontains=estudios)
            
            perfiles = QSusuarios.all()
            serializer = PerfilSerializersSimple(perfiles, many=True)
            print("Usuarios encontrados:", serializer.data)  # Depuración
            return Response(serializer.data)
        else:
            print("Errores del formulario:", formulario.errors)  # Depuración
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "No se recibieron parámetros"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def comentario_busqueda_avanzada(request):

    if not request.user.has_perm("tutorial.view_comentario"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    print("Datos recibidos en query_params:", request.query_params)  # Depuración
    
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaComentarios(request.query_params)
        
        if formulario.is_valid():
            QSusuarios = Comentario.objects.all()  # Inicia con todos los usuarios
            visible = formulario.cleaned_data.get('visible')
            contenido = formulario.cleaned_data.get('contenido')
            puntuacion = formulario.cleaned_data.get('puntuacion')  
            
            if visible is not None:
                QSusuarios = QSusuarios.filter(visible=visible)

            if contenido is not None:
                QSusuarios = QSusuarios.filter(contenido__icontains=contenido)
            
            if puntuacion is not None:
                QSusuarios = QSusuarios.filter(puntuacion=puntuacion)
            
            comentarios = QSusuarios.all()
            serializer = ComentarioSerializersSimple(comentarios, many=True)
            print("Usuarios encontrados:", serializer.data)  # Depuración
            return Response(serializer.data)
        else:
            print("Errores del formulario:", formulario.errors)  # Depuración
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "No se recibieron parámetros"}, status=status.HTTP_400_BAD_REQUEST)

#POST de la API

@api_view(['POST'])
def usuario_create_api(request):

    if not request.user.has_perm("tutorial.add_usuario"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    serializer = UsuarioCreateSerializers(data= request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response ("Usuario Creado")
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response (error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    else: 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def tutorial_create_api(request):

    if not request.user.has_perm("tutorial.add_tutorial"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    serializer = TutorialCreateSerializers(data= request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response ("Tutorial Creado")
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response (error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    else: 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def etiqueta_create_api(request):

    if not request.user.has_perm("tutorial.add_etiqueta"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    serializer = EtiquetaCreateSerializers(data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"message": "Etiqueta creada correctamente"}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:  # ✅ Corrección
            return Response({"error": error.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else: 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def cursos_create_api(request):

    if not request.user.has_perm("tutorial.add_curso"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    serializer = CursosCreateSerializer(data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"message": "Curso creado correctamente"}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:  # ✅ Corrección
            return Response({"error": error.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else: 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_tutorial_api(request):
    # Copiamos los datos que vienen en request.data
    data = request.data.copy()
    # Removemos "usuario" si el cliente lo mandó, para forzar que se use request.user
    if 'usuario' in data:
        data.pop('usuario')

    serializer = TutorialSerializerAPI(data=data, context={'user': request.user})
    if serializer.is_valid():
        try:
            # Guardamos el tutorial asignando el usuario autenticado
            serializer = TutorialSerializerAPI(data=data, context={'user': request.user})
            if serializer.is_valid():
                tutorial = serializer.save()
                return Response(
                    {"message": "Tutorial creado", "id": tutorial.id},
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_curso_api(request):
    data = request.data.copy()
    data.pop('usuario', None)

    serializer = CursosSerializerApi(data=data, context={'user': request.user})
    if serializer.is_valid():
        try:
            curso = serializer.save()
            return Response(
                {"message": "Curso creado correctamente", "id": curso.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # Si aquí no hay return, se produce el None
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # Si no hay return aquí, la vista no retorna nada
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

#PUT de la API

@api_view(['GET'])
def usuario_obtener(request,usuario_id):
    usuario = Usuario.objects
    usuario = usuario.get(id=usuario_id)
    serializer = UsuarioSerializersObtener(usuario)
    return Response(serializer.data)

@api_view(['PUT'])
def usuario_editar_api(request, usuario_id):

    if not request.user.has_perm("tutorial.change_usuario"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    usuario = Usuario.objects.filter(id = usuario_id).first()
    serializer = UsuarioCreateSerializers(data= request.data, instance= usuario)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response('Usuario editado')
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def tutorial_obtener(request,tutorial_id):
    tutorial = Tutorial.objects
    tutorial = tutorial.get(id=tutorial_id)
    serializer = TutorialSerializersObtener(tutorial)
    return Response(serializer.data)

@api_view(['PUT'])
def tutorial_editar_api(request, tutorial_id):

    request.user.refresh_from_db()
    print("Permisos del usuario:", request.user.get_all_permissions())


    if not request.user.has_perm("tutorial.change_tutorial"):
        return Response({"error": "No tienes permisos para ver los Tutoriales."}, status=status.HTTP_403_FORBIDDEN)

    tutorial = Tutorial.objects.filter(id = tutorial_id).first()
    serializer = TutorialCreateSerializers(data= request.data, instance= tutorial)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response('Usuario editado')
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def etiqueta_obtener(request, etiqueta_id):
    etiqueta = Etiqueta.objects.prefetch_related('tutorial').filter(id=etiqueta_id).first()
    
    if not etiqueta:
        return Response({'error': 'Etiqueta no encontrada'}, status=404)

    serializer = EtiquetaSerializersObtener(etiqueta)
    return Response(serializer.data)


@api_view(['PUT'])
def etiqueta_editar_api(request, etiqueta_id):

    if not request.user.has_perm("tutorial.change_etiqueta"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    etiqueta = Etiqueta.objects.filter(id = etiqueta_id).first()
    serializer = EtiquetaCreateSerializers(data= request.data, instance= etiqueta)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response('Etiqueta editado')
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def curso_obtener(request, curso_id):
    curso = Curso.objects.prefetch_related('usuario').filter(id=curso_id).first()
    
    if not curso:
        return Response({'error': 'Curso no encontrada'}, status=404)

    serializer = CursoSerializersObtener(curso)
    return Response(serializer.data)
    
@api_view(['PUT'])
def cursos_editar_api(request, curso_id):

    if not request.user.has_perm("tutorial.change_curso"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    curso = Curso.objects.filter(id = curso_id).first()
    serializer = CursosCreateSerializer(data= request.data, instance= curso)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response('Curso editado')
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
#PATCH de la API

@api_view(['PATCH'])
def usuario_editar_nombre(request, usuario_id):

    if not request.user.has_perm("tutorial.change_usuario"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    usuario = Usuario.objects.filter(id = usuario_id).first()
    serializer = UsuarioSerializerActualizaNombre(data= request.data, instance= usuario)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response('Usuario editado')
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def tutorial_editar_titulo(request, tutorial_id):

    if not request.user.has_perm("tutorial.change_tutorial"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    tutorial = Tutorial.objects.filter(id = tutorial_id).first()
    serializer= TutorialSerializerActualizaTitulo(data = request.data, instance= tutorial)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response('Tutorial editado')
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def etiqueta_editar_nombre(request, etiqueta_id):

    if not request.user.has_perm("tutorial.change_etiqueta"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    etiqueta = Etiqueta.objects.filter(id = etiqueta_id).first()
    serializer= EtiquetaSerializerActualizaNombre(data = request.data, instance= etiqueta)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response('Tutorial editado')
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def cursos_editar_nombre(request, curso_id):

    if not request.user.has_perm("tutorial.change_curso"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    curso = Curso.objects.filter(id = curso_id).first()
    serializer= EtiquetaSerializerActualizaNombre(data = request.data, instance= curso)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response('Curso editado')
        except serializer.ValidationError as error:
            return Response(error.detail, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
#DELETE de la API

@api_view(['DELETE'])
def usuario_eliminar_api (request, usuario_id):

    if not request.user.has_perm("tutorial.delete_usuario"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    usuario = Usuario.objects.filter (id = usuario_id).first()
    if usuario:
        usuario.delete()
        return Response('Usuario eliminado')
    else:
        return Response('Usuario no encontrado', status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def tutorial_eliminar_api (request, tutorial_id):

    if not request.user.has_perm("tutorial.delete_tutorial"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    tutorial= Tutorial.objects.filter (id = tutorial_id).first()
    if tutorial:
        tutorial.delete()
        return Response('Tutorial eliminado')
    else:
        return Response('Tutorial no encontrado', status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def etiqueta_eliminar_api (request, etiqueta_id):

    if not request.user.has_perm("tutorial.delete_etiqueta"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)

    etiqueta= Etiqueta.objects.filter (id = etiqueta_id).first()
    if etiqueta:
        etiqueta.delete()
        return Response('Etiqueta eliminado')
    else:
        return Response('Etiqueta no encontrado', status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def curso_eliminar_api (request, curso_id):

    if not request.user.has_perm("tutorial.delete_usuario"):
        return Response({"error": "No tienes permisos para ver los Usuarios."}, status=status.HTTP_403_FORBIDDEN)
        
    curso= Curso.objects.filter (id = curso_id).first()
    if curso:
        curso.delete()
        return Response('Curso eliminado')
    else:
        return Response('Curso no encontrado', status = status.HTTP_400_BAD_REQUEST)
    
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UsuarioSerializerRegistro(data=request.data)
        if serializer.is_valid():
            try:
                # Convertir el rol a entero para que coincida con las constantes del modelo
                rol_str = request.data.get('rol')
                rol = int(rol_str) if rol_str else None

                # Crear el usuario usando tu modelo personalizado
                user = Usuario.objects.create_user(
                    nombre=request.data.get('nombre'),
                    email=request.data.get('email'),
                    password=request.data.get('password1'),  # password1 viene del serializer
                    rol=rol
                )

                # Asignar grupo y crear registro en la tabla correspondiente (Profesor o Estudiante)
                if rol == Usuario.PROFESOR:
                    grupo = Group.objects.get(name='Profesores')
                    user.groups.add(grupo)
                    profesor, creado = Profesor.objects.get_or_create(usuario=user)
                elif rol == Usuario.ESTUDIANTE:
                    grupo = Group.objects.get(name='Estudiantes')
                    user.groups.add(grupo)
                    estudiante, creado = Estudiante.objects.get_or_create(usuario=user)
                # Si deseas manejar el rol ADMINISTRADOR, podrías añadir un elif más aquí

                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data, status=status.HTTP_201_CREATED)

            except Exception as error:
                print(repr(error))
                return Response(
                    {"detail": f"Ocurrió un error al crear el usuario: {repr(error)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)