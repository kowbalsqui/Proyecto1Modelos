from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class Usuario(AbstractBaseUser):
    ADMINISTRADOR = 1
    PROFESOR = 2
    ESTUDIANTE = 3
    ROLES = (
        (ADMINISTRADOR, 'administrador'),
        (PROFESOR, 'profesor'),
        (ESTUDIANTE, 'estudiante'),
    )

    email = models.EmailField(unique=True)  # Identificador único
    nombre = models.CharField(max_length=30)
    fecha_Registro = models.DateField(null=True, blank=True)
    puntuacion = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    es_activo = models.BooleanField(default=True)
    es_staff = models.BooleanField(default=False)
    es_superuser = models.BooleanField(default=False)
    rol = models.PositiveSmallIntegerField(choices=ROLES, default=ADMINISTRADOR)
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True)

    USERNAME_FIELD = 'email'  # Campo único para autenticación
    REQUIRED_FIELDS = ['nombre']  # Campos obligatorios para createsuperuser

    def __str__(self):
        return self.email

class Profesor(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    

class Estudiante(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    

class Perfil(models.Model):
    bio = models.TextField()
    fecha_Nacimiento = models.DateField()
    REDES = [
        ("IG", "Instagram"),
        ("FB", "Facebook"),
        ("TW", "Twitter"),
        ("LI", "LinkedIn"),
    ]
    redes = models.CharField(choices=REDES, max_length=50)
    estudios = models.TextField(max_length=100)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfiles_Usuarios")
    
    def __str__(self):
        return f"{self.usuario.nombre}"

class Tutorial(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.TextField()
    fecha_Creacion = models.DateTimeField()
    visitas = models.IntegerField()
    valoracion = models.DecimalField(max_digits=3, decimal_places=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_del_tutorial")
    
    def __str__(self):
        return f"{self.usuario.nombre}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    es_activa = models.BooleanField(default=False)
    popularidad = models.DecimalField(max_digits=3, decimal_places=1)
    descripcion = models.TextField(max_length=300)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="categoria_del_tutorial")
    
    def __str__(self):
        return f"{self.tutorial.usuario.nombre}"
    
class SubCategoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=300)
    fecha_Creacion = models.DateTimeField()
    activa = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="CategoriaSubcategoria")
    
    def __str__(self):
        return f"{self.categoria.nombre}"
        

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    publica = models.BooleanField(default=False)
    descripcion = models.TextField(max_length=300)
    tutorial = models.ManyToManyField(Tutorial, related_name="Etiquetas_del_tutorial", through='Etiqueta_tutorial')  # Añadir through
    
    def __str__(self):
        return f"{self.nombre}"

class Favorito(models.Model):
    fecha_Guardado = models.DateTimeField(auto_now=True)
    comentario_Destacado = models.TextField(max_length=300)
    importancia = models.DecimalField(max_digits=3, decimal_places=1)
    notificacion = models.BooleanField(default=False)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="Tutoriales_favoritos")
    usuario = models.ManyToManyField(Usuario, related_name="Favoritos_del_usuario", through='Favorito_usuario')  # Añadir through

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=300)
    horas = models.IntegerField(null = False, blank= False)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    usuario = models.ManyToManyField(Usuario, related_name="usuarios_del_curso")
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="Tutoriales_cursos")
    
    def __str__(self):
        return f"{self.nombre}"
    

class Certificado(models.Model):
    fecha_emision = models.DateField()
    codigo_verificacion = models.CharField(max_length=50)
    nivel = models.IntegerField()
    url_descarga = models.CharField(max_length=50)
    curso = models.OneToOneField(Curso, on_delete=models.CASCADE, related_name="certificado_Curso")
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="Certificado_Usuarios")
    
    def __str__(self):
        return f"{self.usuario.nombre} - {self.curso.nombre}"

class Comentario(models.Model):
    contenido = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    visible = models.BooleanField(default=False)
    puntuacion = models.DecimalField(max_digits=3, decimal_places=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="Comentarios_de_Usuarios")
    
    def __str__(self):
        return f"{self.usuario.nombre}"

# Modelos intermedios personalizados
class Etiqueta_tutorial(models.Model):
    id_etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    id_tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)

class Favorito_usuario(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_favorito = models.ForeignKey(Favorito, on_delete=models.CASCADE)
