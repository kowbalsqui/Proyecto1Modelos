from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UsuarioAdmin(BaseUserAdmin):
    list_display = ('email', 'nombre', 'rol', 'is_staff', 'is_superuser', 'es_activo')
    search_fields = ('email', 'nombre')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'es_activo')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombre', 'imagen', 'fecha_Registro')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Profesor)
admin.site.register(Estudiante)
admin.site.register(Perfil)
admin.site.register(Tutorial)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Etiqueta)
admin.site.register(Favorito)
admin.site.register(Curso)
admin.site.register(Certificado)
admin.site.register(Comentario)

