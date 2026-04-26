from django import forms 
from .models import Viatura, Radio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class ViaturaCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('placa', css_class='form-group col-md-6 mb-0'),
                Column('prefixo', css_class='form-group col-md-6 mb-0'),
    
            ),
            Row(
                Column('modelo', css_class='form-group col-md-6 mb-0'),
            ),
            Column('foto', css_class='form-group col-md-12 mb-0'),
            Row(
                Column('status_viatura_id', css_class='form-group col-md-12 mb-0'),
            ),
        )

    class Meta:
        model = Viatura
        fields = (
            'placa', 
            'modelo', 
            'prefixo', 
            'foto', 
            'status_viatura_id'
        )

class ViaturaChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('placa', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('modelo', css_class='form-group col-md-6 mb-0'),
                Column('prefixo', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('foto', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('status_viatura_id', css_class='form-group col-md-12 mb-0'),
            ),
        )

    class Meta:
        model = Viatura
        fields = (
            'placa', 
            'modelo', 
            'prefixo', 
            'foto', 
            'status_viatura_id'
        )

class RadioCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('prefixo', css_class='form-group col-md-6 mb-0'),
                Column('tipo_radio_id', css_class='form-group col-md-6 mb-0'),
    
            ),
        )

    class Meta:
        model = Radio
        fields = (
            'prefixo', 
            'tipo_radio_id'
        )

class RadioChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('prefixo', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('tipo_radio_id', css_class='form-group col-md-12 mb-0'),
            ),
        )

    class Meta:
        model = Radio
        fields = (
            'prefixo', 
            'tipo_radio_id'
        )