from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=30,)
    email = models.EmailField(max_length=50)
    fecha_Registro = models.DateField(auto_now=True)
    es_activo = models.BooleanField(default=False)
    puntuacion = models.DecimalField(max_digits=3, decimal_places=1)

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

class Tutorial(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.TextField()
    fecha_Creacion = models.DateTimeField(auto_now=True)
    visitas = models.IntegerField()
    valoracion = models.DecimalField(max_digits=3, decimal_places=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_del_tutorial")

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    es_activa = models.BooleanField(default=False)
    popularidad = models.DecimalField(max_digits=3, decimal_places=1)
    descripcion = models.TextField(max_length=300)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="categoria_del_tutorial")

class SubCategoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=300)
    fecha_Creacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="CategoriaSubcategoria")

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    publica = models.BooleanField(default=False)
    descripcion = models.TextField(max_length=300)
    tutorial = models.ManyToManyField(Tutorial, related_name="Etiquetas_del_tutorial", through='Etiqueta_tutorial')  # Añadir through

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

class Certificado(models.Model):
    fecha_emision = models.DateField(auto_now=True)
    codigo_verificacion = models.CharField(max_length=50)
    nivel = models.IntegerField(null= False, blank= False)
    url_descarga = models.CharField(max_length=50)
    curso = models.OneToOneField(Curso, on_delete=models.CASCADE, related_name="certificado_Curso")
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="Certificado_Usuarios")

class Comentario(models.Model):
    contenido = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    visible = models.BooleanField(default=False)
    puntuacion = models.DecimalField(max_digits=3, decimal_places=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="Comentarios_de_Usuarios")

# Modelos intermedios personalizados
class Etiqueta_tutorial(models.Model):
    id_etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    id_tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)

class Favorito_usuario(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_favorito = models.ForeignKey(Favorito, on_delete=models.CASCADE)
