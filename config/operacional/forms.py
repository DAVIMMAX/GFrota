from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Apresentacao

class ApresentacaoCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            Row(
                Column('viatura_id', css_class='form-group col-md-7 mb-0 mx-auto'),
                Column('aeronave_id', css_class='form-group col-md-7 mb-0 mx-auto'),
            ),
            Row(
                Column('turno', css_class='form-group col-md-7  mx-auto mb-0'),
                Column('horario_inicial', css_class='form-group col-md-6 mb-0'),
                Column('horario_final', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('observacao', css_class='form-group col-md-12 mb-0 mx-auto'),
            ),
            Row(
                Column('usuarios', css_class='form-group col-md-12 mb-0 mx-auto'),
            ),
        )

    class Meta:
        model = Apresentacao
        fields = (
            'viatura_id',
            'aeronave_id',
            'turno',
            'horario_inicial',
            'horario_final',
            'observacao',
            'usuarios',
        )
        widgets = {
            'horario_inicial': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'horario_final': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
