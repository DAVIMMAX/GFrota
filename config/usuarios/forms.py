from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            Row(
                Column('nome_completo', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('cpf', css_class='form-group col-md-3 mb-0'),
                Column('matricula', css_class='form-group col-md-3 mb-0'),
                Column('numero_ordem', css_class='form-group col-md-3 mb-0'),
                Column('nome_guerra', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('cargo', css_class='form-group col-md-4 mb-0'),
                Column('orgao_id', css_class='form-group col-md-4 mb-0'),
                Column('funcao', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('roles', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('foto', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
        )

        # Esconde a opção Admin dos perfis (Role) e Funções
        if 'roles' in self.fields:
            self.fields['roles'].queryset = self.fields['roles'].queryset.exclude(nome__icontains='admin')
        if 'funcao' in self.fields:
            self.fields['funcao'].queryset = self.fields['funcao'].queryset.exclude(nome__icontains='admin')

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            'username', 
            'email',
            'nome_completo', 
            'cpf', 
            'matricula', 
            'numero_ordem', 
            'nome_guerra', 
            'cargo', 
            'orgao_id', 
            'funcao',
            'roles',
            'foto'
        )

class UsuarioChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            Row(
                Column('nome_completo', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('cpf', css_class='form-group col-md-3 mb-0'),
                Column('matricula', css_class='form-group col-md-3 mb-0'),
                Column('numero_ordem', css_class='form-group col-md-3 mb-0'),
                Column('nome_guerra', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('cargo', css_class='form-group col-md-4 mb-0'),
                Column('orgao_id', css_class='form-group col-md-4 mb-0'),
                Column('funcao', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('roles', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('foto', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password', css_class='form-group col-md-12 mb-0'),
            ),
        )

        # Esconde a opção Admin dos perfis (Role) e Funções
        if 'roles' in self.fields:
            self.fields['roles'].queryset = self.fields['roles'].queryset.exclude(nome__icontains='admin')
        if 'funcao' in self.fields:
            self.fields['funcao'].queryset = self.fields['funcao'].queryset.exclude(nome__icontains='admin')

    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = (
            'username', 
            'email',
            'nome_completo', 
            'cpf', 
            'matricula', 
            'numero_ordem', 
            'nome_guerra', 
            'cargo', 
            'orgao_id', 
            'funcao',
            'roles',
            'foto'
        )
