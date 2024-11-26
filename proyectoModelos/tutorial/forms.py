from django import forms
from datetime import datetime
from django.forms import ModelForm
from .models import *


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'fecha_Registro', 'es_activo', 'puntuacion']
        labels = {
            "Nombre": ("Nombre del usuario"),
            "Email": ("Correo electrónico"),
            "fecha_Registro": ("Fecha de registro"),
            "es_activo": ("¿Está activo?"),
            "puntuacion": ("Puntuación"),
        }
        widgets = {
            "fecha_Registro":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
    
    def clean (self):
        
        super().clean()
        
        #Primero obtenemos los campos necesarios
        
        nombre = self.cleaned_data.get('nombre')
        email = self.cleaned_data.get('email')
        fecha_Registro = self.cleaned_data.get('fecha_Registro')
        es_activo = self.cleaned_data.get('es_activo')
        puntuacion = self.cleaned_data.get('puntuacion')
        
        #Validamos el campo nombre

        if len(nombre) < 3:
            self.add_error('nombre', 'El nombre debe tener al menos 3 o más caracteres')
        
        #Validamos el campo email
        
        if not email.endswith('@gmail.com'):
            self.add_error('email', 'El email debe terminar con @gmail.com')
        
        #Validamos el campo fecha de registro
        
        if fecha_Registro > datetime.now().date():
            self.add_error('fecha_Registro', 'La fecha de registro no puede ser en el futuro')
        
        #Validamos el campo es_activo
        
        if es_activo is not None and es_activo not in [True, False]:
            self.add_error('es_activo', 'El valor para es_activo debe ser True o False')
        
        #Validamos el campo puntuación
        
        if puntuacion is not None and (puntuacion < 0 or puntuacion > 100):
            self.add_error('puntuacion', 'La puntuación debe estar entre 0 y 100')
        
        return self.cleaned_data