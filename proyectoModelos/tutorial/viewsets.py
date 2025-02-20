from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar usuarios con CRUD completo.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
