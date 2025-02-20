from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar usuarios con CRUD completo.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        if 'password' in request.data:  # 🔹 Verifica si 'password' está en la solicitud
            request.data.pop('password')  # 🔹 Lo elimina si está presente
        return super().create(request, *args, **kwargs)
