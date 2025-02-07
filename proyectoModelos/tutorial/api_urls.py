from django.urls import path
from .api_views import *

urlpatterns = [
    path('tutorial', tutorial_list),
    path('tutorial_simple', tutorial_list_simple),
    path('usuario', usuario_list),
    path('cursos', cursos_list),
    path('categoria', categoria_list),
    path('etiqueta', etiqueta_list),
    path('usuario/busqueda_simple', usuario_busqueda_simple),
    path('usuario/busqueda_avanzada_usuario', usuario_busqueda_avanzada),
    path('tutorial/busqueda_avanzada_tutorial', tutorial_busqueda_avanzado),
    path('perfil', perfil_list),
    path('perfil_simple', perfil_list_simple),
    path('perfil/busqueda_avanzda_perfil', perfil_busqueda_avanzada),
    path('comentario', comentario_list),
    path('comentario_simple', comentario_list_simple),
    path('comentario/busqueda_avanzada_comentario', comentario_busqueda_avanzada),
]