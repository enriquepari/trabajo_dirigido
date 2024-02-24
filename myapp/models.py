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
    archivo = models.FileField(upload_to='documentos/',null=True)
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_archivo