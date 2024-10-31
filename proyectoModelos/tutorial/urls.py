from django.urls import path
from .import views

urlpatterns = [
    path('', views.inicio, name= 'inicio'),
    path('Tutorial/listaTutorial', views.listar_tutoriales, name = 'listar_tutoriales'),
    path('Usuarios/listaUsuario', views.listar_usuarios, name = 'listar_ususario'),
    path('Certificado/Muestra_certificado_de_id_igual_usuario/<int:id_usuario>', views.muestra_certificado_usuario_igual_id, name = 'muestra_certificado_usuario_mismo_id'),
    path('Comentarios/Muestra_comentario_equals_palabra/<str:palabra>', views.muestra_comentario_equals_palabra, name = 'muestra_comentario_equals_palabra')
]