from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path,include
from myapp import views
from django.contrib.auth.views import PasswordResetConfirmView
from myapp.views import login_view,user_list,editar_tramite,reset_password,editar_usuario,send_password_reset_email


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('requisitos/', views.requisitos, name='requisitos'),
    path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('dashboardhome/', views.DashboardViewHome, name='dashboardhome'),
    path('user-list/', user_list, name='user_list'),
    path('register_tramite/', views.crear_tramite, name='register_tramite'),
    path('tramites/', views.listar_tramites, name='listar_tramites'),
    path('editar_tramite/<int:pk>/', editar_tramite, name='editar_tramite'),
    path('editar_usuario/<int:user_id>/', editar_usuario, name='editar_usuario'),
    path('send_password_reset/<int:user_id>/', send_password_reset_email, name='send_password_reset_email'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/<int:user_id>/', reset_password, name='reset_password'),
    path('listar_documentos/', views.listar_documentos, name='listar_documentos'),
    path('subir_documento/<int:tramite_id>/', views.subir_documento, name='subir_documento'),
    path('documentos/<int:documento_id>/', views.ver_contenido_pdf, name='ver_contenido_pdf'),



]
