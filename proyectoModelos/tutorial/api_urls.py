from django.urls import path
from .api_views import *

urlpatterns = [
    path('tutorial', tutorial_list),
    path('usuario', usuario_list),
    path('cursos', cursos_list)
]