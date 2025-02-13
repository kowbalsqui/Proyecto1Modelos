from rest_framework import serializers
from .models import *
from .forms import *

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

class UsuarioCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model: Usuario
        fields= ('nombre', 'email', 'fecha_Registro', 'puntuacion', 'es_activo')
    
    def validate_nombre (self, nombre):
        usuario_nombre = Usuario.objects.filter(nombre= nombre).first()
        if (not usuario_nombre is None):
            if(not self.instance is None and usuario_nombre.id == self.instance.id):
                pass
            else: 
                raise serializers.ValidationError('Ya existe un usuario con ese nombre')
            
        return nombre
    
    def validate_email (self, email):
        usuario_email = Usuario.objects.filter(email = email).first()
        if (not usuario_email is None):
            if(not self.instance is None and usuario_email.id == self.instance.id): 
                pass
            else:
                raise serializers.ValidationError('Ya existe un email resgitrado con ese nombre')
        
        return email
    
    def validate_fecha (self, fecha_Registro):
        fecha_hoy = date.today()
        if fecha_Registro > fecha_hoy or fecha_Registro < fecha_hoy:
            raise serializers.ValidationErrors('No puedes registrarte en cualquier fecha, ingresa la de hoy')
        
        return fecha_Registro
    
    def validate_puntuacion (self, puntuacion):
        if puntuacion > 5:
            raise serializers.ValidationErrors('Solo puedes poner una puntuacion hasta el 5')
        
        return puntuacion
    
    
