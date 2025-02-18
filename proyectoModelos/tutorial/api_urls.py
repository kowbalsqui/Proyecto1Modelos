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
    #crear modelo api
    path('usuario/crear_usuario_api',usuario_create_api),
    path('tutorial/crear_tutorial_api', tutorial_create_api),
    path('etiqueta/crear_etiqueta_api', etiqueta_create_api),
    path('curso/crear_cursos_api', cursos_create_api),
    #obtener modelo api
    path('usuario/<int:usuario_id>',usuario_obtener),
    path('tutorial/<int:tutorial_id>',tutorial_obtener),
    path('etiqueta/<int:etiqueta_id>', etiqueta_obtener), 
    #editar modelo api
    path('usuario/editar/<int:usuario_id>',usuario_editar_api),
    path('usuario/actualizar/nombre/<int:usuario_id>',usuario_editar_nombre),
    path('tutorial/editar/<int:tutorial_id>',tutorial_editar_api),
    path('tutorial/actualizar/titulo/<int:tutorial_id>', tutorial_editar_titulo),
    path('etiqueta/editar/<int:etiqueta_id>',etiqueta_editar_api),
    path('etiqueta/actualizar/nombre/<int:etiqueta_id>', etiqueta_editar_nombre),
    #eliminar modelo api
    path('usuario/eliminar/<int:usuario_id>',usuario_eliminar_api),
    path('tutorial/eliminar/<int:tutorial_id>', tutorial_eliminar_api),
    path('etiqueta/eliminar/<int:etiqueta_id>', etiqueta_eliminar_api),
]