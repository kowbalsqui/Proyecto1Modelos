from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField()
    email = models.EmailField()
    fecha_Registro = models.DateField()
    es_activo = models.BooleanField()
    puntuacion = models.DecimalField()
    
class Perfil (models.Model):
    bio = models.TextField()
    fecha_Nacimiento = models.DateField()
    REDES = [
        ("Instagram"),
        ("Facebook"),
        ("Twitter"),
        ("LinkedIn"),
    ]
    redes = models.CharField(choices=REDES)