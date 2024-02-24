# filters.py
import django_filters
from .models import Tramite

class TramiteFilter(django_filters.FilterSet):
    class Meta:
        model = Tramite
        fields = ['num_tramite', 'solicitante', 'estado']
