from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Apresentacao, ApresentacaoRadio, Ocorrencia, AtribuicaoDoServico, ApresentacaoAtribuicao
from datetime import timedelta
from django.utils import timezone


#forms de apresentacao
class ApresentacaoCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        
        # Personalizar o rótulo dos usuários na lista de seleção
        self.fields['usuarios'].label_from_instance = lambda obj: f"{obj.cargo} {obj.nome_completo or obj.username} | CPF: {obj.cpf or 'N/A'} | Matrícula: {obj.matricula or 'N/A'}"
        self.fields['viatura_id'].label_from_instance = lambda obj: f"{obj.marca} {obj.modelo} - {obj.prefixo} - {obj.placa}"
        self.fields['aeronave_id'].label_from_instance = lambda obj: f"{obj.nome} - {obj.prefixo} - {obj.tipo_aeronave_id}"
        
        
        self.helper.layout = Layout(
            Row(
                Column('tipo_apresentacao', css_class='form-group col-md-12 mb-3 mx-auto'),
            ),
            Row(
                Column('viatura_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Viatura'),
                Column('aeronave_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Aeronave'),
                Column('solo_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Solo'),
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
                Column('usuarios', css_class='form-group col-md-12 mb-4 mx-auto'),
            ),
        )

    class Meta:
        model = Apresentacao
        fields = (
            'tipo_apresentacao',
            'viatura_id',
            'aeronave_id',
            'solo_id',
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

class ApresentacaoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        
        # Personalizar o rótulo dos usuários na lista de seleção
        self.fields['usuarios'].label_from_instance = lambda obj: f"{obj.nome_completo or obj.username} | CPF: {obj.cpf or 'N/A'} | Matrícula: {obj.matricula or 'N/A'}"
        self.fields['viatura_id'].label_from_instance = lambda obj: f"{obj.marca} {obj.modelo} - {obj.prefixo} - {obj.placa}"
        self.fields['aeronave_id'].label_from_instance = lambda obj: f"{obj.prefixo} - {obj.tipo_aeronave_id}"
        
        
        self.helper.layout = Layout(
            Row(
                Column('tipo_apresentacao', css_class='form-group col-md-12 mb-3 mx-auto'),
            ),
            Row(
                Column('viatura_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Viatura'),
                Column('aeronave_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Aeronave'),
                Column('solo_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Solo'),
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
                Column('usuarios', css_class='form-group col-md-12 mb-4 mx-auto'),
            ),
        )

    class Meta:
        model = Apresentacao
        fields = (
            'tipo_apresentacao',
            'viatura_id',
            'aeronave_id',
            'solo_id',
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



class ApresentacaoAtivaUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.fields['usuarios'].label_from_instance = lambda obj: f"{obj.nome_completo or obj.username} | CPF: {obj.cpf or 'N/A'} | Matrícula: {obj.matricula or 'N/A'}"
        self.fields['viatura_id'].label_from_instance = lambda obj: f"{obj.marca} {obj.modelo} - {obj.prefixo} - {obj.placa}"
        self.fields['aeronave_id'].label_from_instance = lambda obj: f"{obj.prefixo} - {obj.tipo_aeronave_id}"
        self.fields['solo_id'].label_from_instance = lambda obj: f"{obj.prefixo} - {obj.tipo_solo_id}"
        self.fields['turno'].label_from_instance = lambda obj: f"{obj.tipo_apresentacao} - {obj.turno}"
        self.fields['horario_inicial'].label_from_instance = lambda obj: f"{obj.horario_inicial.strftime('%d/%m %H:%M')}"
        self.fields['horario_final'].label_from_instance = lambda obj: f"{obj.horario_final.strftime('%d/%m %H:%M')}"
        self.fields['observacao'].label_from_instance = lambda obj: f"{obj.observacao}"

        self.helper.layout = Layout(
            Row(
                Column('tipo_apresentacao', css_class='form-group col-md-12 mb-3 mx-auto'),
            ),
            Row(
                Column('viatura_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Viatura'),
                Column('aeronave_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Aeronave'),
                Column('solo_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Solo'),
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
                Column('usuarios', css_class='form-group col-md-12 mb-4 mx-auto'),
            ),
        )

    class Meta:
        model = Apresentacao
        fields = (
            'tipo_apresentacao',
            'viatura_id',
            'aeronave_id',
            'solo_id',
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

#forms de atribuição
class ApresentacaoAtribuicaoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.fields['usuario_id'].label_from_instance = lambda obj: f"{obj.nome_completo or obj.username} | CPF: {obj.cpf or 'N/A'} | Matrícula: {obj.matricula or 'N/A'}"
        self.fields['apresentacao_id'].label_from_instance = lambda obj: f"{obj.tipo_apresentacao} - {obj.turno}"

        self.helper.layout = Layout(
            Row(
                Column('usuario_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Usuário'),
                Column('apresentacao_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Apresentação'),
                Column('atribuicao_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Atribuição'),
            ),
        )

    class Meta:
        model = ApresentacaoAtribuicao
        fields = (
            'usuario_id',
            'apresentacao_id',
            'atribuicao_id',
        )



#forms de radio
class ApresentacaoRadioUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.fields['usuario_id'].label_from_instance = lambda obj: f"{obj.nome_completo or obj.username} | CPF: {obj.cpf or 'N/A'} | Matrícula: {obj.matricula or 'N/A'}"
        self.fields['radio_id'].label_from_instance = lambda obj: f"{obj.prefixo} - ({obj.tipo_radio_id})"
        self.fields['apresentacao_id'].label_from_instance = lambda obj: f"{obj.tipo_apresentacao} - {obj.turno}"

        self.helper.layout = Layout(
            Row(
                Column('usuario_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Usuário'),
                Column('radio_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Rádio'),
                Column('apresentacao_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Apresentação'),
            ),
        )

    class Meta:
        model = ApresentacaoRadio
        fields = (
            'usuario_id',
            'radio_id',
            'apresentacao_id',
        )
        

class OcorrenciaCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.fields['guarnicoes_id'].label_from_instance = lambda obj: f"{obj.tipo_apresentacao} - {obj.turno} (Início: {obj.horario_inicial.strftime('%d/%m %H:%M')})"
        self.fields['guarnicoes_id'].queryset = Apresentacao.objects.filter(horario_final__gte=timezone.now() - timedelta(hours=24)).order_by('-horario_inicial')

        self.helper.layout = Layout(
            Row(
                Column('tipo_ocorrencia', css_class='form-group col-md-12 mb-3 mx-auto'),
            ),
            Row(
                Column('data_ocorrencia', css_class='form-group col-md-12 mb-0 mx-auto'),
                Column('hora_ocorrencia', css_class='form-group col-md-12 mb-0 mx-auto'),
            ),
            Row(
                Column('guarnicoes_id', css_class='form-group col-md-12 mb-0 mx-auto'),
            ),
            Row(
                Column('observacao', css_class='form-group col-md-12 mb-0 mx-auto'),
            ),
        )

    class Meta:
        model = Ocorrencia
        fields = (
            'tipo_ocorrencia',
            'data_ocorrencia',
            'hora_ocorrencia',
            'guarnicoes_id',
            'observacao',
        )
        widgets = {
            'data_ocorrencia': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'hora_ocorrencia': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }


class ApresentacaoRadioCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.fields['usuario_id'].label_from_instance = lambda obj: f"{obj.nome_completo or obj.username} | CPF: {obj.cpf or 'N/A'} | Matrícula: {obj.matricula or 'N/A'}"
        self.fields['radio_id'].label_from_instance = lambda obj: f"{obj.prefixo} - ({obj.tipo_radio_id})"
        self.fields['apresentacao_id'].label_from_instance = lambda obj: f"{obj.tipo_apresentacao} - {obj.turno}"

        self.helper.layout = Layout(
            Row(
                Column('usuario_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Usuário'),
                Column('radio_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Rádio'),
                Column('apresentacao_id', css_class='form-group col-md-12 mb-0 mx-auto', label='Apresentação'),
            ),
        )

    class Meta:
        model = ApresentacaoRadio
        fields = (
            'usuario_id',
            'radio_id',
            'apresentacao_id',
        )

