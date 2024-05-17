from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from myapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from myapp.views import editar_tramite,reset_password,send_password_reset_email
from django.conf.urls import handler404

handler404 = 'myapp.views.custom_404'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', login_required(views.CustomLogoutView.as_view()), name='logout'),
    path('dashboardhome/', login_required(views.DashboardViewHome), name='dashboardhome'),
    path('user_register/',login_required(views.register), name='user_register'),
    path('perfil/', login_required(views.user_profile), name='user_profile'),
    path('user-list/',login_required(views.user_list), name='user_list'),
    path('user_edit/<int:user_id>/', login_required(views.user_edit), name='user_edit'),
    path('tramite_register/', login_required(views.crear_tramite), name='tramite_register'),
    path('tramite_list/', login_required(views.listar_tramites), name='tramite_list'),
    path('tramite_edit/<int:pk>/', login_required(editar_tramite), name='tramite_edit'),
    path('send_password_reset/<int:user_id>/', login_required(send_password_reset_email), name='send_password_reset_email'),
    path('reset-password/<uidb64>/<token>/', login_required(PasswordResetConfirmView.as_view()), name='password_reset_confirm'),
    path('reset-password/<int:user_id>/', reset_password, name='reset_password'),
    path('tramite_subir_documento/<int:tramite>/', login_required(views.subir_documento), name='tramite_subir_documento'),
    path('documentos/<int:documento_id>/', login_required(views.ver_contenido_pdf), name='ver_contenido_pdf'),
    path('tramite_agregar_observacion/<int:tramite>/', login_required(views.tramite_agregar_observacion), name='tramite_agregar_observacion'),
    path('tramite_ver_observaciones_tramite/<int:tramite_id>/', login_required(views.tramite_ver_observaciones_tramite), name='tramite_ver_observaciones_tramite'),
    path('afiliado_tramite_list/', login_required(views.lista_tramites_afiliados), name='afiliado_tramite_list'),
    path('afiliado_list/', login_required(views.lista_afiliado), name='afiliado_list'),
    path('afiliado_register/<int:tramite_id>/', login_required(views.afiliado_register), name='afiliado_register'),
    path('afiliado_edit/<int:pk>/', login_required(views.editar_afiliado), name='afiliado_edit'),
    path('afiliado_observation/<int:afiliado>/', login_required(views.agregar_observacion), name='afiliado_observation'),
    path('afiliado_ver_observaciones/<int:afiliado_id>/', login_required(views.afiliado_ver_observaciones), name='afiliado_ver_observaciones'),
    path('vehiculos_tramite_list/', views.vehiculos_tramite_list, name='vehiculos_tramite_list'),
    path('vehiculos_register/<int:afiliado_id>/', views.vehiculos_register, name='vehiculos_register'),
    path('vehiculo_list/', views.listar_vehiculos, name='vehiculo_list'),
    path('vehiculos_afiliado_tramite/<int:afiliado_id>/', views.vehiculos_afiliado_tramite, name='vehiculos_afiliado_tramite'),
    path('vehiculo_edit/<int:vehiculo_id>/', views.editar_vehiculo, name='vehiculo_edit'),
    path('vehiculo_informacion/<int:vehiculo_id>/', views.ver_informacion_vehiculo, name='vehiculo_informacion'),
    path('vehiculo_agregar_observaciones/<int:vehiculo_id>/', views.agregar_observaciones, name='vehiculo_agregar_observaciones'),
    path('vehiculo_ver_observaciones/<int:vehiculo_id>/', views.ver_observaciones, name='vehiculo_ver_observaciones'),
    path('tarjeta_operacion_tramite/', views.tarjeta_operacion_tramite, name='tarjeta_operacion_tramite'),
    path('tarjeta_operacion_vehiculo/<int:afiliado_id>/', views.tarjeta_operacion_vehiculo, name='tarjeta_operacion_vehiculo'),
    path('generar_tarjeta_operacion/<int:vehiculo_id>/', views.generar_tarjeta_operacion, name='generar_tarjeta_operacion'),
    path('generar_tarjeta_operacion/<int:vehiculo_id>/', views.generar_tarjeta_operacion, name='generar_tarjeta_operacion'),
    path('detalle_tarjeta_operacion_pdf/<int:tarjeta_operacion_id>/', views.detalle_tarjeta_operacion_pdf, name='detalle_tarjeta_operacion_pdf'),
    path('actualizar_tarjeta_operacion/<int:vehiculo_id>/', views.actualizar_tarjeta_operacion, name='actualizar_tarjeta_operacion'),
    path('verificar_datos_vehiculo/<int:vehiculo_id>/', views.verificar_datos_vehiculo, name='verificar_datos_vehiculo'),
    path('ver_tarjeta_operacion_pdf/<int:tarjeta_operacion_id>/', views.ver_tarjeta_operacion_pdf, name='ver_tarjeta_operacion_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)