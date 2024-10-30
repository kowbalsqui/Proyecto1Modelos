from django.urls import path
from .import views

urlpatterns = [
    path('', views.inicio, name= 'inicio'),
    path('Tutorial/listaTutorial', views.listar_tutoriales, name = 'listar_tutoriales'),
    path('Usuarios/listaUsuario', views.listar_usuarios, name = 'listar_ususario')
    #path('Usuario/listaUserCertificate', views.userCertificate, name = 'userCertificate'),
]