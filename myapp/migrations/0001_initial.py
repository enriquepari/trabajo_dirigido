# Generated by Django 4.2.8 on 2024-02-02 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoTramites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tramite',
            fields=[
                ('num_tramite', models.CharField(max_length=20)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('solicitante', models.CharField(max_length=255)),
                ('num_fojas', models.IntegerField()),
                ('fecha_entrega_form_obs', models.DateField()),
                ('estado', models.CharField(max_length=50)),
                ('comentario', models.TextField()),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_archivo', models.CharField(max_length=255)),
                ('ruta_archivo', models.CharField(max_length=255)),
                ('tipo_tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tipotramites')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tramite')),
            ],
        ),
    ]
