from django.db.models import Q
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from .forms import AfiliadoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.contrib.auth import get_user_model, update_session_auth_hash,login
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.decorators.cache import never_cache
from .forms import MarcaVehiculoForm,VehiculoForm,EditarAfiliadoForm,Tramite, Afiliado,Observaciones_afiliados, Observaciones,Documento,ObservacionForm,TramiteForm,TuFormularioDeEdicion,CustomPasswordResetEmailForm,DocumentoForm,TipoTramiteForm,UserEditForm,CustomUserCreationForm
from django.shortcuts import render
from .forms import ObservacionesAfiliadosForm
from .forms import RazonSocialForm
from django.shortcuts import render, redirect
from .forms import ObservacionesVehiculosForm,AfiliadoForm, RazonSocialForm
from .models import Tramite,Vehiculo,Marca_vehiculo

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboardhome')  

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboardhome')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return redirect('login.html')

@never_cache
@login_required(login_url='login_view')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('user_register') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_register.html', {'form': form})

@never_cache
@login_required(login_url='login_view')
def DashboardViewHome(request):
    user = request.user
    group_name = None
    username = request.user.username
    if user.groups.exists():
        group_name = user.groups.first().name
    return render(request, 'dashboardhome.html')

@never_cache
@login_required(login_url='login_view')
def user_profile(request):
    user = request.user
    groups = user.groups.all()
    return render(request, 'user_profile.html', {'user': user, 'groups': groups})

@never_cache
@login_required(login_url='login_view')
def user_list(request):
    users = User.objects.all()
    groups = Group.objects.all()
    return render(request, 'user_list.html', {'users': users, 'groups': groups})

@never_cache
@login_required(login_url='login_view')
def crear_tramite(request):
    form_t_t = TipoTramiteForm()  
    if request.method == 'POST':
        form_t_t = TipoTramiteForm(request.POST)
        if form_t_t.is_valid():
            form_t_t.save()
            return redirect('tramite_register')
        form_t = TramiteForm(request.POST, user=request.user)
        if form_t.is_valid():
            form_t.instance.usuario = request.user
            tramite = form_t.save(commit=False)
            tramite.save()
            return redirect('tramite_register') 
    else:
        form = TipoTramiteForm()
        form_t = TramiteForm(user=request.user)
        ultimo_tramite = Tramite.objects.order_by('-id').first()
        if ultimo_tramite:
            proximo_numero = ultimo_tramite.id + 1
        else:
            proximo_numero = 1500 
        form_t = TramiteForm(initial={'num_tramite': proximo_numero}, user=request.user)

    context = {
        'form_t_t': form_t_t,
        'form_t': form_t,
    }
    return render(request, 'tramite_register.html', context)

@never_cache
@login_required(login_url='login_view')
def listar_tramites(request):
    query = request.GET.get('q', '')
    tramites = Tramite.objects.all()
    if query:
        tramites = tramites.filter(
            Q(num_tramite__icontains=query) |
            Q(solicitante__icontains=query) |
            Q(estado__icontains=query)
        )
    tramites = tramites.order_by('-id')
    paginator = Paginator(tramites, 10) 
    page = request.GET.get('page')
    try:
        tramites = paginator.page(page)
    except PageNotAnInteger:
        tramites = paginator.page(1)
    except EmptyPage:
        tramites = paginator.page(paginator.num_pages)
    context = {
        'tramites': tramites,
        'query': query,
    }
    return render(request, 'tramite_list.html', context)

@never_cache
@login_required(login_url='login_view')
def listar_tramites(request):
    query = request.GET.get('q', '')
    tramites = Tramite.objects.all()
    if query:
        tramites = tramites.filter(
            Q(num_tramite__icontains=query) |
            Q(solicitante__icontains=query) |
            Q(estado__icontains=query)
        )
    tramites = tramites.order_by('-id')
    paginator = Paginator(tramites, 10)  
    page = request.GET.get('page')
    try:
        tramites = paginator.page(page)
    except PageNotAnInteger:
        tramites = paginator.page(1)
    except EmptyPage:
        tramites = paginator.page(paginator.num_pages)
    context = {
        'tramites': tramites,
        'query': query,
    }
    return render(request, 'tramite_list.html', context)

@never_cache
@login_required(login_url='login_view')
def editar_tramite(request, pk):
    tramite = get_object_or_404(Tramite, pk=pk)
    if request.method == 'POST':
        form = TuFormularioDeEdicion(request.POST, instance=tramite)
        if form.is_valid():
            form.save()
            return redirect('listar_tramites')
    else:
        form = TuFormularioDeEdicion(instance=tramite)
    return render(request, 'tramite_edit.html', {'form': form, 'tramite': tramite})

@never_cache
@login_required(login_url='login_view')
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'user_edit.html', {'form': form, 'user': user})

@never_cache
@login_required(login_url='login_view')
def send_password_reset_email(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomPasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            reset_link = f'http://127.0.0.1:8000/reset-password/{user.id}/'
            subject = 'Restablecimiento de Contraseña'
            html_message = render_to_string('password_reset_email_template.html', {'reset_link': reset_link})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, 'epariaguilar@gmail.com', [email], html_message=html_message)
            messages.success(request, 'Se ha enviado un correo electrónico de restablecimiento de contraseña.')
            return redirect('user_list')
    else:
        form = CustomPasswordResetEmailForm(user=request.user)
    return render(request, 'send_password_reset_email.html', {'form': form, 'user': user})

def reset_password(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña cambiada con éxito.')
            return redirect('user_list')
    else:
        form = SetPasswordForm(user)
    return render(request, 'reset_password.html', {'form': form, 'user': user})

@never_cache
@login_required(login_url='login_view')
def subir_documento(request, tramite):
    tramite = Tramite.objects.get(id=tramite)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, tramite=tramite)
        if form.is_valid():
            documento = form.save()
            return redirect('tramite_list')  
    else:
        form = DocumentoForm(initial={'tramite': tramite.id, 'tramite': tramite.num_tramite})
    return render(request, 'tramite_subir_documento.html', {'form': form, 'tramite': tramite})


@never_cache
@login_required(login_url='login_view')
def ver_contenido_pdf(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    with open(documento.archivo.path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    return response

@never_cache
@login_required(login_url='login_view')
def tramite_agregar_observacion(request, tramite):
    tramite = get_object_or_404(Tramite, id=tramite)
    if request.method == 'POST':
        form = ObservacionForm(request.POST , tramite=tramite)
        if form.is_valid():
                observaciones = form.save()
                return redirect('tramite_list')  
    else:
        form = ObservacionForm(initial={'tramite': tramite.id, 'tramite': tramite.num_tramite})
    return render(request, 'tramite_agregar_observacion.html', {'form': form, 'tramite': tramite})

@never_cache
@login_required(login_url='login_view')
def tramite_ver_observaciones_tramite(request, tramite_id):
    tramite = get_object_or_404(Tramite, id=tramite_id)
    observaciones = Observaciones.objects.filter(tramite=tramite)  
    return render(request, 'tramite_ver_observaciones_tramite.html', {'tramite': tramite, 'observaciones': observaciones})

@never_cache
@login_required(login_url='login_view')
def lista_tramites_afiliados(request):
    tramites = Tramite.objects.all()
    tramites = tramites.order_by('-id')
    tramites_con_afiliado = []
    for tramite in tramites:
        tiene_afiliado = Afiliado.objects.filter(tramite=tramite).exists()
        tramites_con_afiliado.append((tramite, tiene_afiliado))
    return render(request, 'afiliado_tramite_list.html', {'tramites_con_afiliado': tramites_con_afiliado})

@never_cache
@login_required(login_url='login_view')
def lista_afiliado(request):
    afiliados = Afiliado.objects.order_by('-tramite_id')
    return render(request, 'afiliado_list.html', {'afiliados': afiliados})


from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .forms import AfiliadoForm, RazonSocialForm
from .models import Tramite

def afiliado_register(request, tramite_id):
    try:
        tramite = Tramite.objects.get(id=tramite_id)
    except Tramite.DoesNotExist:
        return HttpResponseNotFound("Trámite no encontrado")
    
    if request.method == 'POST':
        form_rs = RazonSocialForm(request.POST)
        if form_rs.is_valid():
            form_rs.save()
            return redirect('afiliado_register', tramite_id=tramite_id)
        
        # Si se envía el formulario principal y es válido, guarda el registro de afiliado
        if 'main-form' in request.POST:
            form = AfiliadoForm(request.POST)
            if form.is_valid():
                afiliado = form.save(commit=False)
                afiliado.tramite = tramite
                afiliado.save()
                return redirect('afiliado_list')
    else:
        form = AfiliadoForm()  
        form_rs = RazonSocialForm()
    
    context2 = {
        'form_rs': form_rs,
        'form': form,
    }
    return render(request, 'afiliado_register.html', context2)

@never_cache
@login_required(login_url='login_view')
def editar_afiliado(request, pk):
    afiliado = get_object_or_404(Afiliado, pk=pk)
    if request.method == 'POST':
        form = EditarAfiliadoForm(request.POST, instance=afiliado)
        if form.is_valid():
            form.save()
            return redirect('listar_tramites')
    else:
        form = EditarAfiliadoForm(instance=afiliado)
    return render(request, 'afiliado_edit.html', {'form': form, 'afiliado': afiliado})

@never_cache
@login_required(login_url='login_view')
def agregar_observacion(request, afiliado):
    afiliado = get_object_or_404(Afiliado, id=afiliado)
    if request.method == 'POST':
        form = ObservacionesAfiliadosForm(request.POST , afiliado=afiliado)
        if form.is_valid():
                observaciones = form.save()
                return redirect('afiliado_list')  
    else:
        form = ObservacionesAfiliadosForm(initial={'tramite': afiliado.id, 'tramite': afiliado.nombre_asociacion})
    return render(request, 'afiliado_observation.html', {'form': form, 'afiliado': afiliado})

@never_cache
@login_required(login_url='login_view')
def afiliado_ver_observaciones(request,afiliado_id):
    afiliado = get_object_or_404(Afiliado, id=afiliado_id)
    observaciones = Observaciones_afiliados.objects.filter(afiliado=afiliado)
    
    return render(request, 'afiliado_ver_observaciones.html', {'afiliado': afiliado, 'observaciones': observaciones})

@never_cache
@login_required(login_url='login_view')

def vehiculos_tramite_list(request):
    tramites_con_afiliado = Afiliado.objects.all()
    datos_tabla = []
    for afiliado in tramites_con_afiliado:
        datos_tramite = {
            'numero_tramite': afiliado.tramite.num_tramite,
            'nombre_afiliado': afiliado.nombre_asociacion,
            'razon_social': afiliado.razon_social_operador.razon_social_operador,
            'afiliado_id': afiliado.id,
        }
        datos_tabla.append(datos_tramite)  
    
    return render(request, 'vehiculos_tramite_list.html', {'datos_tabla': datos_tabla})

from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .forms import VehiculoForm, MarcaVehiculoForm
from .models import Afiliado

def vehiculos_register(request, afiliado_id):
    afiliado = Afiliado.objects.get(id=afiliado_id)
    tramite = afiliado.tramite 
    form_m_v = MarcaVehiculoForm()
    form = VehiculoForm()
    
    if request.method == 'POST':
        form_m_v = MarcaVehiculoForm(request.POST)
        if form_m_v.is_valid():
            form_m_v.save()
            return redirect('vehiculos_register', afiliado_id=afiliado_id)  # Redirige a la misma página
        
        if 'modal-form' in request.POST:  # Verifica si se envió el formulario modal
            form = VehiculoForm(request.POST, request.FILES)
            if form.is_valid():
                vehiculo = form.save(commit=False)
                vehiculo.afiliado = afiliado
                vehiculo.save()
                return redirect('vehiculos_tramite_list')

    context = {
        'form': form,
        'form_m_v': form_m_v,
        'tramite': tramite
    }
    return render(request, 'vehiculos_register.html', context)

from django.shortcuts import render
from .models import Vehiculo

def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculo_list.html', {'vehiculos': vehiculos})

def vehiculos_afiliado_tramite(request, afiliado_id):
    afiliado = Afiliado.objects.get(pk=afiliado_id)
    vehiculos_afiliado = Vehiculo.objects.filter(afiliado=afiliado)
    
    return render(request, 'vehiculos_afiliado_tramite.html', {'afiliado': afiliado, 'vehiculos_afiliado': vehiculos_afiliado})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehiculo
from .forms import VehiculoForm 
from django.contrib import messages

def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos guardados correctamente')
            return render(request, 'vehiculo_edit.html', {'form': form})
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculo_edit.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Vehiculo

def ver_informacion_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    return render(request, 'vehiculo_informacion.html', {'vehiculo': vehiculo})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehiculo

from django.shortcuts import redirect

def agregar_observaciones(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        form = ObservacionesVehiculosForm(request.POST)
        if form.is_valid():
            observaciones = form.save(commit=False)
            observaciones.vehiculo = vehiculo
            observaciones.save()
            # Redirige a la página de detalles del vehículo después de agregar observaciones
            return redirect('vehiculo_ver_observaciones', vehiculo_id=vehiculo_id)
    else:
        form = ObservacionesVehiculosForm()
    return render(request, 'vehiculo_agregar_observaciones.html', {'form': form, 'vehiculo': vehiculo})

from django.shortcuts import render, get_object_or_404
from .models import Vehiculo, Observaciones_vehiculos
def ver_observaciones(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    observaciones = Observaciones_vehiculos.objects.filter(vehiculo=vehiculo)
    return render(request, 'vehiculo_ver_observaciones.html', {'vehiculo': vehiculo, 'observaciones': observaciones})
 
def tarjeta_operacion_tramite(request):
    tramites_con_afiliado = Afiliado.objects.all()
    datos_tabla = []

    for afiliado in tramites_con_afiliado:
        vehiculos_registrados = Vehiculo.objects.filter(afiliado=afiliado).count()

        datos_tramite = {
            'numero_tramite': afiliado.tramite.num_tramite,
            'nombre_afiliado': afiliado.nombre_asociacion,
            'razon_social': afiliado.razon_social_operador.razon_social_operador,
            'afiliado_id': afiliado.id,
            'vehiculos_registrados': vehiculos_registrados,
        }

        datos_tabla.append(datos_tramite)  
    
    return render(request, 'tarjeta_operacion_tramite.html', {'datos_tabla': datos_tabla})

def tarjeta_operacion_vehiculo(request, afiliado_id):
    afiliado = Afiliado.objects.get(pk=afiliado_id)
    vehiculos_afiliado = Vehiculo.objects.filter(afiliado=afiliado)
    
    return render(request, 'tarjeta_operacion_vehiculo.html', {'afiliado': afiliado, 'vehiculos_afiliado': vehiculos_afiliado})

from django.shortcuts import redirect, render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
from io import BytesIO
from .models import TarjetaOperacion

from django.shortcuts import redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
from reportlab.lib.utils import ImageReader
from io import BytesIO
from .models import TarjetaOperacion
from django.shortcuts import redirect
from reportlab.lib.units import cm
from django.urls import reverse
from django.shortcuts import redirect
from reportlab.lib.pagesizes import landscape

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import qrcode
from myapp.models import TarjetaOperacion, Vehiculo
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import qrcode
from myapp.models import TarjetaOperacion, Vehiculo
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
import qrcode
from xhtml2pdf import pisa
from .models import TarjetaOperacion
import io
import base64
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import qrcode
from .models import Vehiculo, TarjetaOperacion
import io
import base64




from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import qrcode
from .models import Vehiculo, TarjetaOperacion

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate
import qrcode
import base64
import io

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import qrcode
import base64
import io
import tempfile

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
import qrcode
import tempfile
import io
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from .models import Vehiculo, TarjetaOperacion

from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import qrcode
import io
import textwrap
import os
from django.core.files.base import ContentFile
from django.http import JsonResponse

def generar_tarjeta_operacion(request, vehiculo_id):
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    afiliado = vehiculo.afiliado
    usuarios_en_grupo_rr = User.objects.filter(groups__name__in=['Registro y Regulación'])
    usuarios_en_grupo_g = User.objects.filter(groups__name__in=['Gobernador'])
    usuarios_en_grupo_j = User.objects.filter(groups__name__in=['Juridico'])
    nombres_apellidos_usuario_rr = ["{} {}".format(usuario.first_name, usuario.last_name) for usuario in usuarios_en_grupo_rr]
    nombres_apellidos_usuario_g = ["{} {}".format(usuario.first_name, usuario.last_name) for usuario in usuarios_en_grupo_g]
    nombres_apellidos_usuario_j = ["{} {}".format(usuario.first_name, usuario.last_name) for usuario in usuarios_en_grupo_j]
    nombres_completo_rr = ", ".join(nombres_apellidos_usuario_rr)
    nombres_completo_g = ", ".join(nombres_apellidos_usuario_g)
    nombres_completo_j = ", ".join(nombres_apellidos_usuario_j)
    marca_vehiculo = vehiculo.marca_vehiculo
    qr_content = f'Placa: {vehiculo.placa}\nChasis: {vehiculo.chasis}\nConductor: {vehiculo.conductor}\nMarca: {vehiculo.marca_vehiculo}\nModelo: {vehiculo.modelo}\nCategoria: {vehiculo.categoria}\nRutas:{vehiculo.rutas}\nValides:{vehiculo.fecha_ve}\nGestion:{vehiculo.gestion}'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_dir = "/ruta/a/tu/carpeta/temporal/"
    if not os.path.exists(qr_img_dir):
        os.makedirs(qr_img_dir)
    qr_img_path = os.path.join(qr_img_dir, f"qr_code_{vehiculo.placa}.png")
    qr_img.save(qr_img_path)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape((19 * cm, 15 * cm))) 
    c.setFont("Helvetica-Bold", 8) 
    c.drawString(1 * cm, 12 * cm, f"OPERADOR: {afiliado.nombre_asociacion}")
    c.drawString(1 * cm, 11.5 * cm, f"PROPIETARIO: {vehiculo.conductor}")
    c.drawString(1 * cm, 11 * cm, f"MODELO: {vehiculo.modelo}")
    c.drawString(7 * cm, 11 * cm, f"CAPACIDAD: {vehiculo.capacidad}")
    c.drawString(1 * cm, 10.5 * cm, f"REGISTRO: {vehiculo.capacidad}")
    c.drawString(7 * cm, 10.5 * cm, f"CHASIS: {vehiculo.chasis}")
    c.drawString(1 * cm, 10 * cm, f"CATEGORIA: {vehiculo.categoria}")
    c.drawString(7 * cm, 10 * cm, f"MARCA: {vehiculo.marca_vehiculo}")
    ruta_text =f"RUTAS: {vehiculo.rutas}"
    ruta_lines = textwrap.wrap(ruta_text, width=100)
    y_position = 8.4 * cm
    for line in ruta_lines:
        c.drawString(1 *cm, y_position,line)
        y_position -= 0.5 *cm
        if y_position < 1 * cm:
            break
    c.setFont("Helvetica-Bold", 11) 
    c.drawString(2 * cm, 9.2 * cm, f"{vehiculo.placa}")
    c.setFont("Helvetica-Bold", 8) 
    c.drawString(1 * cm, 4 * cm, f"LICENCIA VALIDA DEL: {vehiculo.fecha_ve}")    
    c.drawString(8 * cm, 4 * cm, f"AL: {vehiculo.fecha_vvv}")
    c.drawString(5 * cm, 13 * cm, "LICENCIA DE OPERACIONES PARA EL TRANSPORTE")
    c.drawString(7 * cm, 12.5 * cm, "INTERPROVINCIAL")
    c.setFont("Helvetica-Bold", 5) 
    c.drawString(1 * cm, 2.2 * cm, f"{nombres_completo_rr}")
    c.drawString(1 * cm, 1.8 * cm, "REGISTRO Y REGULACION DEL")
    c.drawString(1 * cm, 1.5 * cm, "TRANSPORTE DEPARTAMENTAL")
    c.drawString(8 * cm, 2.2 * cm, f"{nombres_completo_g}")
    c.drawString(8 * cm, 1.8 * cm, "GOBERNADOR DEL DEPARTAMENTO")
    c.drawString(8.5 * cm, 1.5 * cm, "AUTONOMO DE POTOSI")
    c.drawString(14 * cm, 2.2 * cm, f"{nombres_completo_j}")
    c.drawString(14 * cm, 1.8 * cm, "SECRETARIO DEPARTAMENTAL")
    c.drawString(14.5 * cm, 1.5 * cm, "JURIDICO")
    c.setFont("Helvetica", 8) 
    c.rect(1 * cm, 8.9 * cm, 5 * cm, 1 * cm)
    c.drawImage(qr_img_path, 14 * cm, 9 * cm, width=3 * cm, height=3 * cm)  
    c.showPage()
    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    tarjeta_operacion = TarjetaOperacion(vehiculo=vehiculo)
    tarjeta_operacion.pdf.save(f'tarjeta_operacion_{vehiculo.placa}.pdf', ContentFile(pdf_data))
    tarjeta_operacion.save()
    return JsonResponse({'success': True})

def detalle_tarjeta_operacion_pdf(request, tarjeta_operacion_id):
    tarjeta_operacion = get_object_or_404(TarjetaOperacion, id=tarjeta_operacion_id)
    vehiculo = tarjeta_operacion.vehiculo
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="tarjeta_operacion_{vehiculo.placa}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f'Placa: {vehiculo.placa}')
    p.drawString(100, 730, f'Chasis: {vehiculo.chasis}')
    p.drawString(100, 710, f'Conductor: {vehiculo.conductor}')
    p.drawString(100, 690, f'Marca: {vehiculo.marca}')
    p.drawString(100, 670, f'Modelo: {vehiculo.modelo}')
    p.drawString(100, 650, f'Categoría: {vehiculo.categoria}')
    if tarjeta_operacion.qr_code:
        qr_image = tarjeta_operacion.qr_code
        p.drawImage(qr_image.path, 100, 600, width=100, height=100)
    else:
        p.drawString(100, 600, 'QR Code no disponible')
    p.showPage()
    p.save()
    
    return response
from django.shortcuts import render

import os
import io
import qrcode
import textwrap
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from .models import Vehiculo, TarjetaOperacion

def actualizar_tarjeta_operacion(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    tarjeta_operacion = get_object_or_404(TarjetaOperacion, vehiculo=vehiculo)

    qr_content = f'Placa: {vehiculo.placa}\nChasis: {vehiculo.chasis}\nConductor: {vehiculo.conductor}\nMarca: {vehiculo.marca_vehiculo}\nModelo: {vehiculo.modelo}\nCategoria: {vehiculo.categoria}\nRutas:{vehiculo.rutas}\nValides:{vehiculo.fecha_ve}\nGestion:{vehiculo.gestion}'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_dir = os.path.join(settings.BASE_DIR, "ruta", "a", "tu", "carpeta", "temporal")
    if not os.path.exists(qr_img_dir):
        os.makedirs(qr_img_dir)
    qr_img_path = os.path.join(qr_img_dir, f"qr_code_{vehiculo.placa}.png")
    qr_img.save(qr_img_path)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape((15 * cm, 19 * cm)))
    c.setFont("Helvetica-Bold", 10)

    c.drawString(1 * cm, 10 * cm, f"OPERADOR: {vehiculo.afiliado.nombre_asociacion}")
    c.drawString(1 * cm, 9.5 * cm, f"PROPIETARIO: {vehiculo.conductor}")
    c.drawString(1 * cm, 9 * cm, f"MODELO: {vehiculo.modelo}")
    c.drawString(7 * cm, 9 * cm, f"CAPACIDAD: {vehiculo.capacidad}")
    c.drawString(1 * cm, 8.5 * cm, f"REGISTRO: {vehiculo.capacidad}")
    c.drawString(7 * cm, 8.5 * cm, f"CHASIS: {vehiculo.chasis}")
    c.drawString(1 * cm, 8 * cm, f"CATEGORIA: {vehiculo.categoria}")
    c.drawString(7 * cm, 8 * cm, f"MARCA: {vehiculo.marca_vehiculo}")
    ruta_text = f"RUTAS: {vehiculo.rutas}"
    ruta_lines = textwrap.wrap(ruta_text, width=100)
    y_position = 6.4 * cm
    for line in ruta_lines:
        c.drawString(1 * cm, y_position, line)
        y_position -= 0.5 * cm
        if y_position < 1 * cm:
            break

    c.drawString(1 * cm, 4 * cm, f"LICENCIA VALIDA DEL: {vehiculo.fecha_ve}")
    c.drawString(8 * cm, 4 * cm, f"AL: {vehiculo.fecha_vvv}")
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1 * cm, 11 * cm, "TARJETA DE OPERACION")
    c.drawString(2 * cm, 7.2 * cm, f"{vehiculo.placa}")

    c.setFont("Helvetica", 8)
    c.rect(1 * cm, 6.9 * cm, 5 * cm, 1 * cm)
    c.drawImage(qr_img_path, 13 * cm, 10 * cm, width=3 * cm, height=3 * cm)
    c.showPage()
    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()

    # Guardar el PDF actualizado
    tarjeta_operacion.pdf.delete()  # Eliminar el PDF anterior
    tarjeta_operacion.pdf.save(f'tarjeta_operacion_{vehiculo.placa}.pdf', ContentFile(pdf_data))

    return JsonResponse({'success': True})



from django.shortcuts import render
from .models import Vehiculo

def verificar_datos_vehiculo(request, vehiculo_id):
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    # Lógica para verificar los datos del vehículo aquí
    return render(request, 'verificar_datos_vehiculo.html', {'vehiculo': vehiculo})

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import os

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import os

def ver_tarjeta_operacion_pdf(request, tarjeta_operacion_id):
    # Obtener el objeto TarjetaOperacion
    tarjeta_operacion = get_object_or_404(TarjetaOperacion, pk=tarjeta_operacion_id)
    
    # Obtener la ruta del archivo PDF
    pdf_path = tarjeta_operacion.pdf.path
    
    # Abrir el archivo PDF y leer su contenido
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
    
    # Devolver el contenido del PDF como respuesta HTTP
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="%s"' % os.path.basename(pdf_path)
    return response

