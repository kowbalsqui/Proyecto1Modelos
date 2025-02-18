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
        fields = ('id','titulo', 'contenido', 'fecha_Creacion', 'visitas', 'valoracion', 'usuario')

class TutorialSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ('id', 'titulo', 'contenido', 'fecha_Creacion', 'visitas', 'valoracion')
        
#clase cursos serializers

class CursosSerializer(serializers.ModelSerializer):
    #Paras las relaciones One y Many to One
    usuario = UsuarioSerializer(many = True)
    class Meta:
        model = Curso
        fields = ('id', 'nombre', 'descripcion', 'horas', 'precio', 'usuario')

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
        fields = ('id', 'nombre', 'color', 'publica', 'descripcion', 'tutorial')

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
    
#Serializer obtener modelo

class UsuarioSerializersObtener(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombre', 'email', 'fecha_Registro', 'puntuacion', 'es_activo')
    
class TutorialSerializersObtener(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ('titulo', 'contenido', 'fecha_Creacion', 'visitas', 'valoracion', 'usuario')
    
class EtiquetaSerializersObtener(serializers.ModelSerializer):
    tutorial = TutorialSerializer(many=True)  # Asegura que traiga varios tutoriales
    class Meta:
        model = Etiqueta
        fields = ('nombre', 'color', 'publica', 'descripcion', 'tutorial')

class CursoSerializersObtener(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=True)  # Asegura que traiga varios tutoriales
    class Meta:
        model = Curso
        fields = ('id', 'nombre', 'descripcion', 'horas', 'precio', 'usuario')


#Serializer crear modelo
class UsuarioCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
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
    
class TutorialCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ('titulo', 'contenido', 'fecha_Creacion', 'visitas', 'valoracion', 'usuario')
    
    def validate_titulo(self, titulo):
        tutorial_titulo = Tutorial.objects.filter(titulo=titulo).first()
        if (not tutorial_titulo is None):
            if (not self.instance is None and tutorial_titulo.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un tutorial con ese titulo')
        return titulo
    
    def validate_contenido(self, contenido):
        if len(contenido) > 50:
            raise serializers.ValidationError('El contenido no puede tener más de 50 caracteres')
        return contenido
    
    def validate_fecha(self, fecha_Creacion):
        fecha_hoy = date.today()
        if fecha_Creacion > fecha_hoy or fecha_Creacion < fecha_hoy:
            raise serializers.ValidationErrors('No puedes registrar una fecha diferente a la de hoy')
        return fecha_Creacion
    
    def validate_visitas(self, visitas):   
        if visitas < 0:
            raise serializers.ValidationErrors('Las visitas no pueden ser negativas')
        return visitas
    
    def validate_valoracion(self, valoracion):
        if valoracion > 5:
            raise serializers.ValidationErrors('La valoracion no puede ser mayor a 5')
        return valoracion
    
    def validate_usuario(self, usuario):
        if not usuario:  # Verifica si es None
            raise serializers.ValidationError("El usuario no puede estar vacío.")
        return usuario

class EtiquetaCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ('nombre', 'color', 'publica', 'descripcion', 'tutorial')

    def validate_nombre(self, nombre):
        etiqueta_nombre = Etiqueta.objects.filter(nombre=nombre).first()
        if etiqueta_nombre is not None:
            if self.instance is not None and etiqueta_nombre.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe una etiqueta con ese nombre')
        return nombre

    def validate_color(self, color):
        if not color.startswith('#') or len(color) != 7:
            raise serializers.ValidationError('El color debe ser un código hexadecimal válido')
        return color

    def validate_publica(self, publica):
        if not isinstance(publica, bool):
            raise serializers.ValidationError('El campo publica debe ser un valor booleano')
        return publica

    def validate_descripcion(self, descripcion):
        if len(descripcion) > 100:
            raise serializers.ValidationError('La descripción no puede tener más de 100 caracteres')
        return descripcion

    def create(self, validated_data):
        tutoriales = self.initial_data.get('tutorial', [])

        if not tutoriales:  # Verifica que al menos hay un tutorial
            raise serializers.ValidationError({'tutorial': ['Debe seleccionar al menos un tutorial']})

        etiqueta = Etiqueta.objects.create(
            nombre=validated_data["nombre"],
            color=validated_data["color"],
            publica=validated_data["publica"],
            descripcion=validated_data["descripcion"],
        )

        # 🔹 Asigna tutoriales a la etiqueta correctamente
        etiqueta.tutorial.set(Tutorial.objects.filter(id__in=tutoriales))

        return etiqueta
    
    def update(self, instance, validated_data):
        tutoriales = self.initial_data.get('tutorial', [])

        if not tutoriales:
            raise serializers.ValidationError({'tutorial': ['Debe seleccionar al menos un tutorial']})

        instance.nombre = validated_data["nombre"]
        instance.color = validated_data["color"]
        instance.publica = validated_data["publica"]
        instance.descripcion = validated_data["descripcion"]
        instance.save()

        # 🔹 Limpia y asigna tutoriales correctamente
        instance.tutorial.set(Tutorial.objects.filter(id__in=tutoriales))

        return instance

class CursosCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Curso
        fields = ('nombre', 'descripcion', 'horas', 'precio', 'usuario')

    def validate_nombre(self, nombre):
        if len(nombre) < 3:
            raise serializers.ValidationError('El nombre debe tener al menos 3 caracteres')
        return nombre

    def validate_descripcion(self, descripcion):
        if len(descripcion) > 200:
            raise serializers.ValidationError('La descripción no puede tener más de 200 caracteres')
        return descripcion

    def validate_horas(self, horas):
        if horas <= 0:
            raise serializers.ValidationError('Las horas deben ser un número positivo')
        return horas

    def validate_precio(self, precio):
        if precio < 0:
            raise serializers.ValidationError('El precio no puede ser negativo')
        return precio

    def validate_usuario(self, usuario):
        """✅ Asegura que `usuario` sea una lista antes de validar."""
        if not isinstance(usuario, list):  # 🔹 Evita `TypeError`
            raise serializers.ValidationError('El campo usuario debe ser una lista de IDs válidos.')

        if len(usuario) < 1:
            raise serializers.ValidationError('Debe seleccionar al menos un usuario.')
        
        return usuario



#Serializer editar modelo
class UsuarioSerializerActualizaNombre(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombre',)
        
    def validate_nombre(self, nombre):
        usuario_nombre = Usuario.objects.filter(nombre=nombre).first()
        if (not usuario_nombre is None):
            if (not self.instance is None and usuario_nombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un usuario con ese nombre')
            
        return nombre

class TutorialSerializerActualizaTitulo(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields= ('id', 'titulo')
    
    def validate_titulo(self, titulo):
        tutorial_titulo = Tutorial.objects.filter(titulo=titulo).first()
        if (not tutorial_titulo is None):
            if (not self.instance is None and tutorial_titulo.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un tutorial con ese titulo')
        return titulo
    
class EtiquetaSerializerActualizaNombre(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields= ('id', 'nombre')
    
    def validate_nombre(self, nombre):
        etiqueta_nombre = Etiqueta.objects.filter(nombre=nombre).first()
        if (not etiqueta_nombre is None):
            if (not self.instance is None and etiqueta_nombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un Etiqueta con ese titulo')
        return nombre
    
class CursoSerializerActualizaNombre(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields= ('id', 'nombre')
    
    def validate_nombre(self, nombre):
        curso_nombre = Curso.objects.filter(nombre=nombre).first()
        if (not curso_nombre is None):
            if (not self.instance is None and curso_nombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un Curso con ese titulo')
        return nombre
    
