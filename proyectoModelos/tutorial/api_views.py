from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

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