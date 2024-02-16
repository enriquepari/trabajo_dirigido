from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PasswordResetEmailForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import TramiteForm
from .forms import TuFormularioDeEdicion
from .models import Tramite
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PasswordResetEmailForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def home(request):
    return render(request, 'home.html')

def requisitos(request):
    return render(request, 'requisitos.html')

def ubicacion(request):
    return render(request, 'ubicacion.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboardhome')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})  
    
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('register') 
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect('home')
@login_required

def DashboardViewHome(request):
    user = request.user
    group_name = None
    username = request.user.username
    if user.groups.exists():
        group_name = user.groups.first().name

    return render(request, 'dashboardhome.html', {'username': username,'group_name': group_name})

def user_list(request):
    users = User.objects.all()
    groups = Group.objects.all()
    return render(request, 'user_list.html', {'users': users, 'groups': groups})

def crear_tramite(request):
    if request.method == 'POST':
        form = TramiteForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.usuario = request.user
            tramite = form.save(commit=False)
            tramite.save()
            return redirect('register_tramite') 
    else:
        form = TramiteForm(user=request.user)
        ultimo_tramite = Tramite.objects.order_by('-id').first()
        if ultimo_tramite:
            proximo_numero = ultimo_tramite.id + 1
        else:
            proximo_numero = 1500 
        form = TramiteForm(initial={'num_tramite': proximo_numero}, user=request.user)
    return render(request, 'register_tramite.html', {'form': form})

def listar_tramites(request):
    query = request.GET.get('q', '')
    tramites = Tramite.objects.all().order_by('-id')
    if query:
        tramites = tramites.filter(
            Q(num_tramite__icontains=query) |
            Q(solicitante__icontains=query) |
            Q(estado__icontains=query)
        )

    context = {
        'tramites': tramites,
        'query': query,
    }

    return render(request, 'listar_tramites.html', context)

def editar_tramite(request, pk):
    tramite = get_object_or_404(Tramite, pk=pk)

    if request.method == 'POST':
        form = TuFormularioDeEdicion(request.POST, instance=tramite)
        if form.is_valid():
            form.save()
            return redirect('listar_tramites')
    else:
        form = TuFormularioDeEdicion(instance=tramite)

    return render(request, 'editar_tramite.html', {'form': form, 'tramite': tramite})

def editar_usuario(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'editar_usuario.html', {'form': form, 'usuario': user})

def send_password_reset_email(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Lógica para generar un token único (puedes usar Django's TokenGenerator)
            # ...

            # Lógica para construir el enlace de restablecimiento de contraseña
            reset_link = f'http://127.0.0.1:8000/reset-password/{user.id}/'

            # Construir el cuerpo del correo electrónico usando una plantilla HTML
            subject = 'Restablecimiento de Contraseña'
            html_message = render_to_string('password_reset_email_template.html', {'reset_link': reset_link})
            plain_message = strip_tags(html_message)

            # Enviar el correo electrónico
            send_mail(subject, plain_message, 'epariaguilar@gmail.com', [email], html_message=html_message)

            messages.success(request, 'Se ha enviado un correo electrónico de restablecimiento de contraseña.')
            return redirect('user_list')
    else:
        form = PasswordResetEmailForm()

    return render(request, 'send_password_reset_email.html', {'form': form, 'user': user})


# myapp/views.py
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

def reset_password(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualizar la sesión para evitar cerrar la sesión del usuario
            messages.success(request, 'Contraseña cambiada con éxito.')
            return redirect('user_list')
    else:
        form = SetPasswordForm(user)

    return render(request, 'reset_password.html', {'form': form, 'user': user})



