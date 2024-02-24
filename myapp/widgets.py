from django import forms

class TipoTramiteWidget(forms.Select):
    template_name = 'widgets/tipo_tramite_widget.html'

class TipoTramiteChoiceField(forms.ModelChoiceField):
    widget = TipoTramiteWidget