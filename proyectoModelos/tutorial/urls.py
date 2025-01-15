from django.urls import path, re_path
from .import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.inicio, name= 'inicio'),
    path('Tutorial/listaTutorial', views.listar_tutoriales, name = 'listar_tutoriales'),
    path('Usuarios/listaUsuario', views.listar_usuarios, name = 'listar_ususario'),
    path('Certificado/Muestra_certificado_de_id_igual_usuario/<int:id_usuario>', views.muestra_certificado_usuario_igual_id, name = 'muestra_certificado_usuario_mismo_id'),
    path('Comentarios/Muestra_comentario_equals_palabra/<str:palabra>', views.muestra_comentario_equals_palabra, name = 'muestra_comentario_equals_palabra'),
    re_path(r'^Tutorial/muestra_tutorial_por_etiqueta/([A-Z][a-zA-Z]{3,})/$', views.muestra_tutorial_por_etiqueta, name='muestra_tutorial_por_etiqueta'),
    path('Usuarios/Lista_usuarios_entre_años/<int:año1>/<int:año2>', views.lista_usuarios_entre_años, name = 'lista_usuarios_entre_años'),
    path('Tutorial/Lista_tutorial_por_categoria/<str:categoria1>/<str:categoria2>', views.lista_tutorial_por_categoria, name = 'lista_tutorial_por_categoria'),
    path('Tutorial/Total_visitas', views.total_visitas, name = 'total_visitas'),
    path('Tutorial/tutorial_no_tenga_categoria', views.tutorial_no_tenga_categoria, name = 'tutorial_no_tenga_categoria'),
    path('Subcategoria/Lista_subcategoria', views.lista_subcategoria, name = 'lista_subcategoria'),
    #CREAR
    path('formulario/usuarioFormulario', views.usuario_Form, name = 'usuarioFormulario'),
    path('formulario/perfilFormulario', views.perfil_Form, name = 'perfilFormulario'),
    path('formulario/tutorialFormulario', views.tutorial_Form, name = "tutorialFormulario"),
    path('formulario/subcategoriaFormulario', views.subcategoria_Form, name = "subcategoriaFormulario"),
    path('formulario/comentarioFomulario', views.comentario_Form, name = "comentarioFomulario"),
    path('formulario/certificadoFormulario', views.certificado_Form, name = "certificadoFomulario"),
    path('enlaces/', views.pagina_de_enlaces, name='pagina_de_enlaces'),
    path('buscar/', views.busqueda_avanzada, name='buscar'),
    #BUSQUEDA
    path('formulario/filtros-avanzados/', views.filtros_avanzados, name='filtros_avanzados'),
    path('formulario/filtros-avanzados-tutoriales/', views.filtros_avanzados_tutoriales, name='filtros_avanzados_tutoriales'),
    path('formulario/filtros-avanzados-perfil/', views.filtros_avanzados_perfil, name = 'filtros_avanzados_perfil'),
    path('formulario/filtros-avanzados-subcategorias/', views.filtrosAvanzadosSubcategorias, name = 'filtros_avanzados_subcategorias'),
    path('formulario/filtros-avanzados-comentarios/', views.filtrosAvanzadosComentarios, name= 'filtros_avanzados_comentarios'),    
    path('formulario/filtros-avanzados-certificados/', views.filtrosAvanzadosCertificados, name= 'filtros_avanzados_certificados'),
    #URL DE MODIFICAR
    path('formulario/usuario-modificar/<int:usuario_id>', views.usuario_modificar,name="usuario_modificar"),
    path('formulario/tutorial-modificar/<int:tutorial_id>', views.tutorial_modificar,name="tutorial_modificar"),
    path('formulario/perfil-modificar/<int:perfil_id>', views.perfil_modificar,name="perfil_modificar"),
    path('formulario/subcategoria-modificar/<int:subcategoria_id>', views.subcategoria_modificar,name="subcategoria_modificar"),
    path('formulario/comentario-modificar/<int:comentario_id>', views.comentario_modificar,name="comentario_modificar"),
    path('formulario/certificado-modificar/<int:certificado_id>', views.certificado_modificar,name="certificado_modificar"),
    #URL DE BORRAR
    path('formulario/usuario-eliminar/<int:usuario_id>',views.eliminar_usuario,name='eliminar_usuario'),
    path('formulario/tutorial-eliminar/<int:tutorial_id>',views.eliminar_tutorial,name='eliminar_tutorial'),
    path('formulario/perfil-eliminar/<int:perfil_id>',views.eliminar_perfil,name='eliminar_perfil'),
    path('formulario/subcategoria-eliminar/<int:subcategoria_id>',views.eliminar_subcategoria,name='eliminar_subcategoria'),
    path('formulario/comentario-eliminar/<int:comentario_id>',views.eliminar_comentario,name='eliminar_comentario'),
    path('formulario/certificado-eliminar/<int:certificado_id>',views.eliminar_certificado,name='eliminar_certificado'),
    #URL RegistrarUser
    path('registrar', views.registrar_usuario, name= 'registrar_usuario'),
    #URL IniciarSesion
    path('login', LoginView.as_view(), name='login'),  # vista de inicio de sesión
    path('logout', LogoutView.as_view(), name='logout'),  # vista de cierre de sesión
]