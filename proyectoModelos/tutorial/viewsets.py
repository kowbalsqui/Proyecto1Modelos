from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """ Devuelve los datos del usuario autenticado """
        return Response(UsuarioSerializer(request.user, context={'request': request}).data)

