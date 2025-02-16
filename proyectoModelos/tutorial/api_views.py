from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from django.db.models import Q,Prefetch
from rest_framework import status

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
    cursos = Curso.objects.all()
    serializers = CursosSerializer(cursos, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def comentario_list(request):
    comentario = Comentario.objects.all()
    serializers = ComentarioSerializers(comentario, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def comentario_list_simple(request):
    comentario = Comentario.objects.all()
    serializers = ComentarioSerializers(comentario, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def perfil_list(request):
    perfil = Perfil.objects.all()
    serializers = PerfilSerializers(perfil, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def perfil_list_simple(request):
    perfil = Perfil.objects.all()
    serializers = PerfilSerializersSimple(perfil, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def categoria_list(request):
    categoria = Categoria.objects.all()
    serializers = CategoriaSerializer(categoria, many = True)
    return Response(serializers.data)

@api_view (['GET'])
def etiqueta_list(request):
    etiqueta = Etiqueta.objects.all()
    serializers = EtiquetaSerializer(etiqueta, many = True)
    return Response(serializers.data)

@api_view(['GET'])
def usuario_busqueda_simple(request):
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
def usuario_busqueda_avanzada(request):
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
    
from rest_framework import serializers  # 🔹 Importar serializers

@api_view(['POST'])
def etiqueta_create_api(request):
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

#PUT de la API

@api_view(['GET'])
def usuario_obtener(request,usuario_id):
    usuario = Usuario.objects
    usuario = usuario.get(id=usuario_id)
    serializer = UsuarioSerializersObtener(usuario)
    return Response(serializer.data)

@api_view(['PUT'])
def usuario_editar_api(request, usuario_id):
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
    
#PATCH de la API

@api_view(['PATCH'])
def usuario_editar_nombre(request, usuario_id):
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
    
#DELETE de la API

@api_view(['DELETE'])
def usuario_eliminar_api (request, usuario_id):
    usuario = Usuario.objects.filter (id = usuario_id).first()
    if usuario:
        usuario.delete()
        return Response('Usuario eliminado')
    else:
        return Response('Usuario no encontrado', status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def tutorial_eliminar_api (request, tutorial_id):
    tutorial= Tutorial.objects.filter (id = tutorial_id).first()
    if tutorial:
        tutorial.delete()
        return Response('Tutorial eliminado')
    else:
        return Response('Tutorial no encontrado', status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def etiqueta_eliminar_api (request, etiqueta_id):
    etiqueta= Etiqueta.objects.filter (id = etiqueta_id).first()
    if etiqueta:
        etiqueta.delete()
        return Response('Etiqueta eliminado')
    else:
        return Response('Etiqueta no encontrado', status = status.HTTP_400_BAD_REQUEST)