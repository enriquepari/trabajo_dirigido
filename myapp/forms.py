from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
from .models import Marca_vehiculo,Observaciones_vehiculos, Tramite,Vehiculo,Observaciones,Razon_social, Afiliado, Observaciones_afiliados,Tipo_tramite,Documento

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
        'password_too_short': "La contraseña debe tener al menos 8 caracteres.",
        'password_common': "La contraseña no puede ser una contraseña común.",
        'password_entirely_numeric': "La contraseña no puede ser completamente numérica.",
        'password_similar': "La contraseña no puede ser demasiado similar a tu otra información personal.",
        'username_exists': "Este nombre de usuario ya está en uso. Elige otro.",
    }

    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Tu contraseña debe tener al menos 8 caracteres y no puede ser demasiado común.",
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Ingresa la misma contraseña que antes, para verificación.",
    )
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        help_text="Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.",
    )
    first_name = forms.CharField(
        label="Nombre ",
        max_length=150,
        help_text="Requerido. Ponga su primer nombre.",
    )
    last_name = forms.CharField(
        label="Apellidos ",
        max_length=150,
        help_text="Requerido. Ingrese su apellido.",
    )
    email = forms.CharField(
        label="Correo electronico ",
        max_length=150,
        help_text="Requerido. Introduzca una dirección de correo electrónico válida.",
    )
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'groups']
     
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        help_text="Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.",
    )
    first_name = forms.CharField(
        label="Nombre del usuario",
        max_length=150,
    )
    last_name = forms.CharField(
        label="Apellido del usuario",
        max_length=150,
    )
    email = forms.CharField(
        label="Correo electronico",
        max_length=150,
    )

class TramiteForm(forms.ModelForm):

    class Meta:
        model = Tramite
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'readonly': 'readonly'}),
            'fecha_entrega_form_obs': forms.DateInput(attrs={'readonly': 'readonly'}),
            'hora': forms.TimeInput(attrs={'readonly': 'readonly'}),
            'num_tramite': forms.TextInput(attrs={'readonly': 'readonly'}),
            'tipo_de_tramite':  forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['num_tramite'].widget.attrs['readonly'] = True
        tz = pytz.timezone('America/La_Paz')

        self.initial['fecha'] = timezone.now().astimezone(tz).date()
        self.initial['fecha_entrega_form_obs'] = timezone.now().astimezone(tz).date()
        self.initial['hora'] = timezone.now().astimezone(tz).strftime('%H:%M')
        if user:
            self.fields['usuario'].initial = user.id
            self.fields['usuario'].widget.attrs['disabled'] = True

        widget=forms.TextInput(attrs={'type': 'button', 'value': '+', 'class': 'plus-button'}),
        required=False
        
class TuFormularioDeEdicion(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = ['num_tramite', 'fecha', 'hora', 'solicitante', 'num_fojas','tipo_de_tramite', 'fecha_entrega_form_obs', 'estado', 'comentario', 'usuario']
    num_tramite = forms.CharField(required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha_entrega_form_obs = forms.DateField(required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha = forms.DateField(required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    hora = forms.TimeField(required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=False, disabled=True)

    def clean_fecha(self):
        return self.instance.fecha

class CustomPasswordResetEmailForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()

        if not user:
            raise forms.ValidationError('Este correo electrónico no está asociado a ningún usuario.')

        return email

class TipoTramiteForm(forms.ModelForm):
    class Meta:
        model = Tipo_tramite
        fields = ['nom_tipo_de_tramite']

class DocumentoForm(forms.ModelForm):

    class Meta:
        model = Documento
        fields = ['nombre_archivo', 'archivo', 'tramite']
        widgets = {
            'tramite': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        tramite = kwargs.pop('tramite', None)
        super().__init__(*args, **kwargs)

        if tramite:
            self.initial['tramite'] = tramite.id

            self.fields['tramite'].widget.attrs['readonly'] = True


class ObservacionForm(forms.ModelForm):
    class Meta:
        model = Observaciones
        fields = ['espacio', 'fecha_obs', 'hora_obs', 'tramite']
        widgets = {
            'espacio': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': 'Ingrese la observación aquí'}),
            'fecha_obs': forms.DateInput(attrs={'readonly': 'readonly'}),
            'hora_obs': forms.TimeInput(attrs={'readonly': 'readonly'}),
            'tramite': forms.TextInput(attrs={'readonly': 'readonly'}),

        }

    def __init__(self, *args, **kwargs):
        tramite = kwargs.pop('tramite', None)
        super(ObservacionForm, self).__init__(*args, **kwargs)
        self.fields['espacio'].label = 'Observación'
        tz = pytz.timezone('America/La_Paz')

  
        self.initial['fecha_obs'] = timezone.now().astimezone(tz).date()
        self.initial['hora_obs'] = timezone.now().astimezone(tz).strftime('%H:%M')
        if tramite:
            self.fields['tramite'].initial = tramite.id
            self.fields['tramite'].widget.attrs['disabled'] = True
           
        required=False

class RazonSocialForm(forms.ModelForm):
    class Meta:
        model = Razon_social
        fields = ['razon_social_operador']

class AfiliadoForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = ['nombre_asociacion', 'razon_social_operador', 'fecha', 'hora', 'ubicacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'readonly': 'readonly'}),
            'hora': forms.TimeInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tz = pytz.timezone('America/La_Paz')

        self.initial['fecha'] = timezone.now().astimezone(tz).date()
        self.initial['hora'] = timezone.now().astimezone(tz).strftime('%H:%M')
        

class EditarAfiliadoForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = ['nombre_asociacion', 'razon_social_operador', 'fecha', 'hora', 'ubicacion']

class ObservacionesAfiliadosForm(forms.ModelForm):
    class Meta:
        model = Observaciones_afiliados
        fields = ['espacio', 'fecha_obs', 'hora_obs', 'afiliado']
        widgets = {
            'espacio': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': 'Ingrese la observación aquí'}),

        }

    def __init__(self, *args, **kwargs):
        afiliado = kwargs.pop('afiliado', None)
        super(ObservacionesAfiliadosForm, self).__init__(*args, **kwargs)

        self.fields['espacio'].label = 'Observación'
        tz = pytz.timezone('America/La_Paz')

  
        self.initial['fecha_obs'] = timezone.now().astimezone(tz).date()
        self.initial['hora_obs'] = timezone.now().astimezone(tz).strftime('%H:%M')
from .models import Vehiculo
from django.utils import timezone
import pytz

class MarcaVehiculoForm(forms.ModelForm):
    class Meta:
        model = Marca_vehiculo
        fields = ['marca_vehiculo']


from django import forms
from .models import Vehiculo
from django.utils import timezone
import pytz

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'botic', 'conductor', 'fecha_ve', 'fecha_vvv', 'hora_ve', 'categoria', 
                  'capacidad', 'tipo_de_vehiculo', 'marca_vehiculo', 'modelo', 'chasis', 'imagen', 
                  'tipo_tarjeta', 'validez', 'gestion', 'rutas']
        widgets = {
            'fecha_ve': forms.DateInput(attrs={'readonly': 'readonly'}),
            'hora_ve': forms.TimeInput(attrs={'readonly': 'readonly'}),
            'fecha_vvv': forms.DateInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tz = pytz.timezone('America/La_Paz')
        afiliado = self.initial.get('afiliado')
        if afiliado:
            self.initial['botic'] = afiliado.tramite.num_tramite

        self.initial['fecha_ve'] = timezone.now().astimezone(tz).date()
        self.initial['hora_ve'] = timezone.now().astimezone(tz).strftime('%H:%M')

        fecha_ve = self.initial.get('fecha_ve')
        if fecha_ve:
            self.initial['fecha_vvv'] = fecha_ve.replace(year=fecha_ve.year + 1)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class ObservacionesVehiculosForm(forms.ModelForm):
    class Meta:
        model = Observaciones_vehiculos
        fields = ['espacio', 'fecha_obs', 'hora_obs', 'vehiculo']
        widgets = {
            'espacio': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': 'Ingrese la observación aquí'}),

        }

    def __init__(self, *args, **kwargs):
        vehiculo = kwargs.pop('vehiculo', None)
        super(ObservacionesVehiculosForm, self).__init__(*args, **kwargs)

        self.fields['espacio'].label = 'Observación'
        tz = pytz.timezone('America/La_Paz')

  
        self.initial['fecha_obs'] = timezone.now().astimezone(tz).date()
        self.initial['hora_obs'] = timezone.now().astimezone(tz).strftime('%H:%M')
        if vehiculo:
            self.initial['vehiculo'] = vehiculo.matricula

            self.fields['vehiculo'].widget.attrs['readonly'] = False


