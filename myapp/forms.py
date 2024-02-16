from django import forms
from django.utils import timezone
from .models import Tramite
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import pytz


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


class TramiteForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'readonly': 'readonly'}),
            'fecha_entrega_form_obs': forms.DateInput(attrs={'readonly': 'readonly'}),
            'hora': forms.TimeInput(attrs={'readonly': 'readonly'}),
            'num_tramite': forms.TextInput(attrs={'readonly': 'readonly'}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        tz = pytz.timezone('America/La_Paz')

        self.initial['fecha'] = timezone.now().astimezone(tz).date()
        self.initial['fecha_entrega_form_obs'] = timezone.now().astimezone(tz).date()
        self.initial['hora'] = timezone.now().astimezone(tz).strftime('%H:%M')
        if user:
            self.fields['usuario'].initial = user.id
            self.fields['usuario'].widget.attrs['disabled'] = True

class TuFormularioDeEdicion(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = ['num_tramite', 'fecha', 'hora', 'solicitante', 'num_fojas', 'fecha_entrega_form_obs', 'estado', 'comentario', 'usuario']
    num_tramite = forms.CharField(required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha_entrega_form_obs = forms.DateField(required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha = forms.DateField(required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    hora = forms.TimeField(required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=False, disabled=True)

    def clean_fecha(self):
        return self.instance.fecha

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico')
