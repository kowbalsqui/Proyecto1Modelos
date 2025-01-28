from rest_framework import serializers
from .models import *

#clase usuario serializer

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

#clase Tutorial serializers

class TutorialSerializer(serializers.ModelSerializer):
    #Para relaciones OneToOne o ManyToOne
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Tutorial
        fields = ('titulo', 'contenido', 'fecha_Creacion', 'visitas', 'valoracion', 'usuario')
        
#clase cursos serializers

class CursosSerializer(serializers.ModelSerializer):
    #Paras las relaciones One y Many to One
    usuario = UsuarioSerializer()
    tutorial = TutorialSerializer()
    
    class Meta:
        model = Curso
        fields = ('nombre', 'descripcion', 'horas', 'precio', 'usuario', 'tutorial')