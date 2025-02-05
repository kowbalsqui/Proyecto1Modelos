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

class TutorialSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ('titulo', 'contenido', 'fecha_Creacion', 'visitas', 'valoracion')
        
#clase cursos serializers

class CursosSerializer(serializers.ModelSerializer):
    #Paras las relaciones One y Many to One
    tutorial = TutorialSerializer()
    class Meta:
        model = Curso
        fields = ('nombre', 'descripcion', 'horas', 'precio', 'tutorial')

#clase categoria serializers

class CategoriaSerializer(serializers.ModelSerializer):
    #Para las relaciones One y Many to One
    tutorial = TutorialSerializer()
    class Meta:
        model = Categoria
        fields = ('nombre', 'es_activa', 'popularidad', 'descripcion', 'tutorial')

#clase etiqueta serializers

class EtiquetaSerializer(serializers.ModelSerializer):
    #Para las relaciones ManyToMany
    tutorial = TutorialSerializer(many=True)
    class Meta:
        model = Etiqueta
        fields = ('nombre', 'color', 'publica', 'descripcion', 'tutorial')

class PerfilSerializers(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=True)

    class Meta:
        model = Perfil
        fields = ('bio', 'fecha_Nacimiento', 'redes', 'estudios', 'usuario')
    
class PerfilSerializersSimple(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ('bio', 'fecha_Nacimiento', 'redes', 'estudios')


class ComentarioSerializers(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=True)

    class Meta:
        model = Comentario
        fields = ('contenido', 'fecha', 'visible', 'puntuacion', 'usuario')

class ComentarioSerializersSimple(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ('contenido', 'fecha', 'visible', 'puntuacion')
