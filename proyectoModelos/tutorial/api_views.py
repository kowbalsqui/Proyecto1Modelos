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
            nombre = formulario.cleaned_data.get('nombre')
            activo = formulario.cleaned_data.get('es_activo')
            puntuacion = formulario.cleaned_data.get('puntuacion')
            
            if nombre:
                QSusuarios = QSusuarios.filter(nombre__icontains=nombre)
            
            if puntuacion is not None:
                if 1 <= puntuacion <= 5:
                    QSusuarios = QSusuarios.filter(puntuacion=puntuacion)
            
            if activo is not None:
                QSusuarios = QSusuarios.filter(es_activo=activo)
            
            usuarios = QSusuarios.all()
            serializer = UsuarioSerializer(usuarios, many=True)
            print("Usuarios encontrados:", serializer.data)  # Depuración
            return Response(serializer.data)
        else:
            print("Errores del formulario:", formulario.errors)  # Depuración
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "No se recibieron parámetros"}, status=status.HTTP_400_BAD_REQUEST)
