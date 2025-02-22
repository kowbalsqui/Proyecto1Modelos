"""
URL configuration for proyectoModelos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from tutorial.viewsets import UsuarioViewSet

#añadir este import
#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#    TokenRefreshView,
#)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)  # ⬅️ Registra el ViewSet en la API

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tutorial.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/', include("tutorial.api_urls")),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(router.urls)),  # ⬅️ Incluye todas las rutas generadas automáticamente
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)