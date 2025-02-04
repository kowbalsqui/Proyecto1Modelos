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

@api_view (['GET'])
def usuario_busqueda_simple (request):
    if (request.user.has_perm('tutorial.view_usuario')):
        form = BusquedaSimpleUsuario(request.query_params)
        if form.is_valid():
            texto = form.data.get('textoBusqueda')
            usuario = Usuario.objects.filter(Q(nombre__icontains = texto) | Q(email__icontains = texto))
            serializer = UsuarioSerializer(usuario, many = True)
            return Response(serializer.data)
        else:
            return Response(form.errors, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'Sin permisos'}, status = status.HTTP_400_BAD_REQUEST)