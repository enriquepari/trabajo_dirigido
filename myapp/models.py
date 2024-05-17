from django.db import models
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Tipo_tramite(models.Model):
    nom_tipo_de_tramite = models.CharField(max_length=255)
    def __str__(self):
        return self.nom_tipo_de_tramite
    

class Tramite(models.Model):
    num_tramite = models.CharField(max_length=20, unique=True, blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    solicitante = models.CharField(max_length=255)
    num_fojas = models.IntegerField()
    tipo_de_tramite = models.ForeignKey(Tipo_tramite, on_delete=models.CASCADE, null=True, blank=True)
    fecha_entrega_form_obs = models.DateField()
    ESTADO_CHOICES = [
        ('Ingresado', 'Ingresado'),
        ('Anulado', 'Anulado'),
        ('Entregado', 'Entregado'),
        ('Proceso', 'Proceso')
        ]
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    comentario = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.num_tramite = max(1500, Tramite.objects.all().count() + 1500)

        super().save(*args, **kwargs)
    def __str__(self):
        return self.num_tramite
    

class Documento(models.Model):
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='pdf/', blank=True, null=True)
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_archivo
    
class Observaciones(models.Model):
    espacio = models.TextField()
    fecha_obs = models.DateField()
    hora_obs = models.TimeField()
    tramite = models.ForeignKey('Tramite', on_delete=models.CASCADE)

    def __str__(self):
        return f'Observación para Trámite {self.tramite.num_tramite}'


class Razon_social(models.Model):
    razon_social_operador = models.CharField(max_length=100)
    def __str__(self):
        return self.razon_social_operador
    
    
class Afiliado(models.Model):
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
    nombre_asociacion = models.CharField(max_length=100)
    razon_social_operador = models.ForeignKey(Razon_social, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_asociacion

class Observaciones_afiliados(models.Model):
    espacio = models.TextField()
    fecha_obs = models.DateField()
    hora_obs = models.TimeField()
    afiliado = models.ForeignKey('Afiliado', on_delete=models.CASCADE)

    def __str__(self):
        return f'Observación para Afiliado {self.afiliado.nombre_asociacion}'
    
from django.db import models
class Marca_vehiculo(models.Model):
    marca_vehiculo = models.CharField(max_length=100)
    def __str__(self):
        return self.marca_vehiculo
    
     
class Vehiculo(models.Model):
    afiliado = models.ForeignKey(Afiliado, on_delete=models.CASCADE)
    marca_vehiculo = models.ForeignKey(Marca_vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    placa = models.CharField(max_length=20)
    botic = models.CharField(max_length=100)
    conductor = models.CharField(max_length=100)
    fecha_ve = models.DateField()
    fecha_vvv = models.DateField()
    hora_ve = models.TimeField()
    categoria = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    tipo_de_vehiculo = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    chasis = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    tipo_tarjeta = models.CharField(max_length=100)
    validez = models.CharField(max_length=100)
    gestion = models.CharField(max_length=100)
    rutas = models.TextField()

    def __str__(self):
        return self.placa

class Observaciones_vehiculos(models.Model):
    espacio = models.TextField()
    fecha_obs = models.DateField()
    hora_obs = models.TimeField()
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)

    def __str__(self):
        return f'Observación para vehiculo {self.vehiculo.placa}'

from django.db import models
class TarjetaOperacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='pdf_tarjetas_operacion/')
