from django import forms
from datetime import datetime
from django.forms import ModelForm
from .models import *
from django.utils.timezone import now
from datetime import date, timedelta
from datetime import datetime


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'fecha_Registro', 'es_activo', 'puntuacion', 'imagen']
        labels = {
            "Nombre": ("Nombre del usuario"),
            "Email": ("Correo electrónico"),
            "fecha_Registro": ("Fecha de registro"),
            "es_activo": ("¿Está activo?"),
            "puntuacion": ("Puntuación"),
            "imagen": ("Imagen")
        }
        widgets = {
            "fecha_Registro":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        super().clean()
    
    # Primero obtenemos los campos necesarios
        nombre = self.cleaned_data.get('nombre')
        email = self.cleaned_data.get('email')
        fecha_Registro = self.cleaned_data.get('fecha_Registro')
        es_activo = self.cleaned_data.get('es_activo')
        puntuacion = self.cleaned_data.get('puntuacion')
        
        
    
    # Validamos el campo nombre
        if nombre and len(nombre) < 3:
            self.add_error('nombre', 'El nombre debe tener al menos 3 o más caracteres')
        
        # Validamos el campo email
        if email and not email.endswith('@gmail.com'):
            self.add_error('email', 'El email debe terminar con @gmail.com')
        
        # Validamos el campo fecha de registro
        if fecha_Registro and fecha_Registro > datetime.now().date():
            self.add_error('fecha_Registro', 'La fecha de registro no puede ser en el futuro')
        
        # Validamos el campo es_activo
        if es_activo is not None and es_activo not in [True, False]:
            self.add_error('es_activo', 'El valor para es_activo debe ser True o False')
        
        # Validamos el campo puntuación
        if puntuacion is not None and (puntuacion < 0 or puntuacion > 100):
            self.add_error('puntuacion', 'La puntuación debe estar entre 0 y 100')
        
        return self.cleaned_data
    
class PerfilForm (ModelForm):
    class Meta:
        model = Perfil
        fields = ['bio', 'fecha_Nacimiento', 'redes', 'estudios', 'usuario']
        labels = {
            "Bio": ("Bio"),
            "Fecha de nacimiento": ("Fecha de nacimiento"),
            "Redes": ("Redes sociales"),
            "Estudios": ("Estudios"),
            "Usuario" : ("Usuario")
        }
        widgets = {
        "fecha_Nacimiento":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
        
    def clean (self):
        
        super().clean()
        
        #Primero obtenemos los campos necesarios
        
        bio = self.cleaned_data.get('bio')
        redes = self.cleaned_data.get('redes')
        fecha_Nacimiento = self.cleaned_data.get('fecha_Nacimiento')
        estudios = self.cleaned_data.get('estudios')
        
        #Validamos el campo bio

        if len(bio) < 2:
            self.add_error('La biografia debe tener como maximo 100 caracteres')
        
        #Validamos el campo redes
        
        if redes not in ["IG", "FB", "TW", "LI"]:
            self.add_error('redes', 'Ninguna red coincide con las disponibles, repita')
            
        #Validamos el campo fecha de nacimiento
        
        if fecha_Nacimiento > datetime.now().date():
            self.add_error('fecha_Nacimiento', 'La fecha de nacimiento no puede ser en un futuro')
            
        #Validamos el campo estudios
        
        if not estudios:
            self.add_error('estudios', 'El campo de estudios no puede esta vacio, requiere de minino un titulo')

        return self.cleaned_data

class TutorialForm(ModelForm):
    class Meta:
        model = Tutorial
        fields = ['titulo', 'contenido', 'fecha_Creacion', 'visitas', 'valoracion', 'usuario']
        labels = {
            "titulo": "Título",
            "contenido": "Contenido",
            "fecha_Creacion": "Fecha de creación",
            "visitas": "Número de visitas",
            "valoracion": "Valoración (0-5)",
            "usuario": "Usuario asociado"
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Introduce el título"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "placeholder": "Escribe el contenido", "rows": 5}),
            "fecha_Creacion": forms.DateInput(
                format="%Y-%m-%d", 
                attrs={"type": "date", "class": "form-control"}
            ),
            "visitas": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "valoracion": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 5, "step": 0.1}),
            "usuario": forms.Select(attrs={"class": "form-control"}),
        }
        
    def clean (self):
        
        super().clean()
        
        #Primero obtenemos los campos necesarios
        
        titulo = self.cleaned_data.get('titulo')
        contenido = self.cleaned_data.get('contenido')
        fecha_Creacion = self.cleaned_data.get('fecha_Creacion')
        visitas = self.cleaned_data.get('visitas')
        valoracion = self.cleaned_data.get('valoracion')
        
        #Validamos el campo titulo
        
        if len(titulo) < 5:
            self.add_error('titulo', 'El título debe tener como minimo 5 caracteres')
        
        #Validamos el campo contenido
        
        if len(contenido) < 10:
            self.add_error('contenido', 'El contenido debe tener como minimo 10 caracteres')
        
        #Validamos el campo fecha de creacion
        
        if fecha_Creacion > datetime.now():
            self.add_error('fecha_Creacion', 'La fecha de creación no puede ser en un futuro')
        
        #Validamos el campo visitas
        
        if visitas < 0:
            self.add_error('visitas', 'El número de visitas no puede ser negativo')
        
        #Validamos el campo valoracion
        
        if valoracion < 0 or valoracion > 5:
            self.add_error('valoracion', 'La valoración debe estar entre 0 y 5')
            
        return self.cleaned_data

class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = SubCategoria
        fields = ['nombre', 'descripcion', 'fecha_Creacion', 'categoria', 'activa']
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "fecha_Creacion": "Fecha de creación",
            "categoria": "Categoría",
            "activa": "Está activa?"
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Escribe la descripción", "rows": 5}),
            "fecha_Creacion": forms.DateInput(
                format="%Y-%m-%d", 
                attrs={"type": "date", "class": "form-control"}
            ),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "activa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        
        def clean (self):
            
            super().clean()
            
            #Primero obtenemos los campos necesarios
            
            nombre = self.cleaned_data.get('nombre')
            descripcion = self.cleaned_data.get('descripcion')
            fecha_Creacion = self.cleaned_data.get('fecha_Creacion')
            categoria = self.cleaned_data.get('categoria')
            activa = self.cleaned_data.get('activa')
            
            #Validamos el campo nombre
            
            if len(nombre) < 3:
                self.add_error('nombre', 'El nombre no puede tener menos de 3 caracteres')
            
            #Validamos el campo descripcion
            
            if len(descripcion) < 10:
                self.add_error('descripcion', 'La descripción debe tener como minimo 10 caracteres')
            
            #Validamos el campo fecha_creacion
            
            if fecha_Creacion > datetime.now().date():
                self.add_error('fecha_Creacion', 'La fecha de creación no puede ser en un futuro')
            
            #Validamos el campo categoria
            
            if categoria is None:
                self.add_error('categoria', 'Debe seleccionar una categoría')
            
            #Validamos el campo es_activa
            
            if activa is None:
                self.add_error('activa', 'Debe seleccionar si está activa')
                
            return self.cleaned_data
        
class ComentarioForm(ModelForm):
    class Meta: 
        model = Comentario
        fields = ['contenido', 'fecha', 'visible', 'puntuacion', 'usuario']
        labels = {
            "contenido": "Contenido",
            "fecha": "Fecha",
            "visible": "Visible?",
            "puntuacion": "Puntuación (0-5)",
            "usuario": "Usuario asociado"
        }
        widgets = {
            "contenido": forms.Textarea(attrs={"class": "form-control", "placeholder": "Escribe el contenido", "rows": 5}),
            "fecha": forms.DateInput(
                format="%Y-%m-%d", 
                attrs={"type": "date", "class": "form-control"}
            ),
            "visible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "puntuacion": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 5, "step": 0.1}),
            "usuario": forms.Select(attrs={"class": "form-control"}),
        }
        
    def clean (self):
        
        super().clean()
        
        #Primero obtenemos los campos necesarios
        
        contenido = self.cleaned_data.get('contenido')
        fecha =self.cleaned_data.get('fecha')
        visible = self.cleaned_data.get('viisble')
        puntuacion = self.cleaned_data.get('puntuacion')
        
        #Validamos el campo contenido
        
        if len(contenido) < 10:
            self.add_error('contenido', 'El contenido debe tener como minimo 10 caracteres')
        
        #Validamos el campo fecha
        
        if fecha > datetime.now():
            self.add_error('fecha', 'La fecha no puede ser en un futuro')
        
        #Validamos el campo visible
        
        if visible:
            self.add_error('visible', 'Debe seleccionar si está visible')
        
        #Validamos el campo puntuacion
        
        if puntuacion < 0 or puntuacion > 5:
            self.add_error('puntuacion', 'La puntuación debe estar entre 0 y 5')
            
        return self.cleaned_data
    
class CertificadoForm(ModelForm):
    class Meta:
        model= Certificado
        fields = ['fecha_emision', 'codigo_verificacion', 'nivel', 'url_descarga', 'curso', 'usuario']
        labels = {
            "fecha_emision": "Fecha de emisión",
            "codigo_verificacion": "Código de verificación",
            "nivel": "Nivel",
            "url_descarga": "URL de descarga",
            "curso": "Curso asociado",
            "usuario": "Usuario asociado"
        }
        widgets = {
            "fecha_emision": forms.DateInput(
                format="%Y-%m-%d", 
                attrs={"type": "date", "class": "form-control"}
            ),
            "codigo_verificacion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Introduce el código de verificación"}),
            "nivel": forms.TextInput(attrs={"class": "form-control", "placeholder": "Introduce el nivel"}),
            "url_descarga": forms.URLInput(attrs={"class": "form-control", "placeholder": "Introduce la URL de descarga"}),
            "curso": forms.Select(attrs={"class": "form-control"}),
            "usuario": forms.Select(attrs={"class": "form-control"}),
        }
        
        def clean (self):
            
            super().clean()
            
            #Primero obtenemos los campos necesarios
            
            fecha_emision = self.cleaned_data.get('fecha_emision')
            codigo_verificacion = self.cleaned_data.get('codigo_verificacion')
            nivel = self.cleaned_data.get('nivel')
            url_descarga = self.cleaned_data.get('url_descarga')
            
            #Validamos el campo fecha_emision
            
            if fecha_emision > datetime.now().date():
                self.add_error('fecha_emision', 'La fecha no puede ser a futuros de hoy')
            
            #Validamos el campo codigo_verificacion
            
            if len(codigo_verificacion) != 6:
                self.add_error('codigo_verificacion', 'El código de verificación debe tener 6 caracteres')
            
            #Validamos el campo nivel
            
            if len(nivel) < 3:
                self.add_error('nivel', 'El nivel debe tener como minimo 3 caracteres')
            
            #Validamos el campo url_descarga
            
            if not url_descarga.startswith("http"):
                self.add_error('url_descarga', 'La URL de descarga debe comenzar con http:// o https://')
                
            return self.cleaned_data
        
        
class BusquedaAvanzadaForm(forms.Form):
    # Campos de búsqueda para Usuario
    nombre = forms.CharField(max_length=100, required=False, label="Nombre")
    email = forms.EmailField(required=False, label="Email")
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Registro (Desde)")
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Registro (Hasta)")
    imagen = forms.ImageField(required=False)
    
    # Campos de búsqueda para otro modelo, por ejemplo, Curso
    curso_nombre = forms.CharField(max_length=100, required=False, label="Nombre del Curso")

    #Camnpos de busqueda para tutoriales

    tutorial_titulos = forms.CharField(max_length=100, required=False, label="Nombre del Tutorial")

    #Campos de busqueda para comentarios

    comentario_contenido = forms.CharField(max_length=100, required=False, label="Palabra de comentario")
    
    # Selección del tipo de búsqueda
    tipo_busqueda = forms.ChoiceField(choices=[('usuario', 'Usuario'), ('curso', 'Curso'), ('tutorial', 'Tutorial'), ('comentario', 'Comentario')], required=True, label="Tipo de Búsqueda")

class BusquedaAvanzadaUsuario(forms.Form):
    puntuacion = forms.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 5.0'
        })
    )
    es_activo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    fecha_Registro = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )

    def clean(self):
        super().clean()

        puntuacion = self.cleaned_data.get('puntuacion')
        activo = self.cleaned_data.get('es_activo')
        fecha_Registro = self.cleaned_data.get('fecha_Registro')

        if not puntuacion and not activo and not fecha_Registro:
            self.add_error('puntuacion', 'Debes rellenar un campo minimo')
            self.add_error('es_activo', 'Debes rellenar un campo minimo')
            self.add_error('fecha_Registro', 'Debes rellenar un campo minimo')

        # Validación de puntuación (verifica si no es None)
        if puntuacion is not None:
            if puntuacion < 1 or puntuacion > 5:
                self.add_error('puntuacion', 'La puntuación debe estar entre 1 y 5.')

        # Validación de activo (puede ser None)
        if activo is None:
            self.add_error('activo', 'Debe especificar si el usuario está activo o no.')

        # Validación de fecha de registro
        if fecha_Registro:
            if fecha_Registro > now().date():
                self.add_error('fecha_Registro', 'La fecha no puede estar en el futuro.')

        return self.cleaned_data

class BusquedaAvanzadaTutorial(forms.Form):
    visitas = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1'
        })
    )
    valoracion = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1'
        })
    )
    usuario = forms.ModelChoiceField(
    queryset=Usuario.objects.all(),
    required=False,
    widget=forms.Select(attrs={
        'class': 'form-control'
    })
)

    def clean(self):
        super().clean()

        visitas = self.cleaned_data.get('visitas')
        valoracion = self.cleaned_data.get('valoracion')
        usuario = self.cleaned_data.get('usuario')

        if not visitas and not valoracion and not usuario:
            self.add_error('visitas',"Debes rellenar al menos un dato: visitas, valoración o usuario.")
            self.add_error('valoracion',"Debes rellenar al menos un dato: visitas, valoración o usuario.")
            self.add_error('usuario',"Debes rellenar al menos un dato: visitas, valoración o usuario.")

        # Validación de visitas
        if visitas is not None and visitas < 0:
            self.add_error('visitas', 'El número de visitas no puede ser negativo.')

        # Validación de valoración
        if valoracion is not None and valoracion < 0:
            self.add_error('valoracion', 'El número de valoraciones no puede ser negativo.')

        # Validación de usuario (no aplica error si está vacío porque es opcional)
        # Si lo haces obligatorio, asegúrate de que esté seleccionado
        if usuario is not None and not Usuario.objects.filter(id=usuario.id).exists():
            self.add_error('usuario', 'Seleccione un usuario válido.')

        return self.cleaned_data
    

class BusquedaAvanzadaPerfil(forms.Form):
    fecha_Nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )
    redes = forms.ChoiceField(
        choices=Perfil.REDES,  
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    estudios = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Estudios superiores',
        })
    )

    def clean(self):
        super().clean()

        fecha_Nacimiento = self.cleaned_data.get('fecha_Nacimiento')
        redes = self.cleaned_data.get('redes')
        estudios = self.cleaned_data.get('estudios')
        hoy = date.today()
        limite_inferior = hoy - timedelta(days=365 * 100)  # 100 años atrás
        limite_superior = hoy + timedelta(days=365 * 100)  # 100 años adelante

        # Validación global: al menos un campo debe estar relleno
        if not fecha_Nacimiento and not redes and not estudios:
                self.add_error('fecha_Nacimiento', 'Debes rellenar un campo minimo')
                self.add_error('redes', 'Debes rellenar un campo minimo')
                self.add_error('estudios', 'Debes rellenar un campo minimo')

        # Validación de fecha de nacimiento
        if fecha_Nacimiento:
            if fecha_Nacimiento < limite_inferior or fecha_Nacimiento > limite_superior:
                self.add_error('fecha_Nacimiento', 'La fecha de nacimiento debe estar entre 100 años atrás y adelante.')

        return self.cleaned_data
    
class BusquedaAvanzadaSubcategorias(forms.Form):
    nombre = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
    })
    )
    activa = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    def clean (self):
        super().clean()

        nombre = self.cleaned_data.get('nombre')
        activa = self.cleaned_data.get('activa')
        categoria = self.cleaned_data.get('categoria')

        if not nombre and not activa and not categoria:
            self.add_error('nombre', 'Debe haber al menos un campo relleno')
            self.add_error('activa', 'Debe haber al menos un campo relleno')
            self.add_error('categoria', 'Debe haber al menos un campo relleno')
        
        if activa is None:
            self.add_error('activa', 'Debe especificar si el usuario está activo o no.')

        return self.cleaned_data

class BusquedaAvanzadaComentarios(forms.Form):
    contenido = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contenido...',
        })
    )
    visible = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    puntuacion = forms.DecimalField(
        max_digits=3,
        decimal_places=1,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 5.0',
        })
    )

    def clean(self):
        super().clean()

        contenido = self.cleaned_data.get('contenido')
        visible = self.cleaned_data.get('visible')
        puntuacion = self.cleaned_data.get('puntuacion')

        # Validación: Al menos un campo debe estar rellenado
        if not contenido and not visible and not puntuacion:
            self.add_error('contenido', 'Se debe rellenar minimo un campo')
            self.add_error('visible', 'Se debe rellenar minimo un campo')
            self.add_error('puntuacion', 'Se debe rellenar minimo un campo')

        # Validación de puntuación
        if puntuacion is not None and puntuacion < 0:
            self.add_error('puntuacion', 'La puntuación no puede ser menor que 0 o negativa.')

        return self.cleaned_data

class BusquedaAvanzadaCertificados(forms.Form):
    codigo_verificacion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Codigo...',
        })
    )
    nivel = forms.IntegerField(
        required= False,
        widget= forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nivel...',
        })
    )
    fecha_emision = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )

    def clean(self):
        super().clean()

        codigo_verificacion = self.cleaned_data.get('codigo_verificacion')
        nivel = self.cleaned_data.get('nivel')
        fecha_emision = self.cleaned_data.get('fecha_emision')

        if not codigo_verificacion and not nivel and not fecha_emision:
            self.add_error('codigo_verificacion', 'Se debe rellenar minimo un campo')
            self.add_error('nivel', 'Se debe rellenar minimo un campo')
            self.add_error('fecha_emision', 'Se debe rellenar minimo un campo')
        
        return self.cleaned_data