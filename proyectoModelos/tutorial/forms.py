from django import forms

class UsuarioForm(forms.Form):
    #Definimos el campo nombre del usuario para el formulario
    nombre = forms.CharField(
        label='Nombre de usuario',
        required= True,
        max_length=100,
        help_text='Nombre de usuario'
    )
    
    #Definimos el campo email del usuario para el fomulario
    
    email = forms.EmailField(
        label='Correo de usuario',
        required = True,
        max_length=100,
        help_text='Correo de usuario'
    )
    
    #Definimos el campo Fecha de registro del usuario para el formulario
    
    fecha_Registro = forms.DateField(
        label='Fecha de registro',
        required= True,
        help_text='Fecha de registro'
    )
    
    #Definimos el campo es_activo del usuario para el formulario
    
    es_activo = forms.BooleanField(
        label='¿Está activo?',
        required= False,
        help_text='Indica si el usuario está activo'
    )
    
    #Definimos el campo puntuación del usuario para el formulario
    
    puntuacion = forms.IntegerField(
        label='Puntuación',
        required= False,
        help_text='Puntuación del usuario'
    )
    