from django.db import models
from django.contrib.auth.models import AbstractUser

class Orgao(models.Model):
    orgao = models.CharField(max_length=255, verbose_name='Órgão')

    class Meta:
        verbose_name = 'Órgão'
        verbose_name_plural = 'Órgãos'

    def __str__(self):
        return self.orgao


class Role(models.Model):
    role = models.CharField(max_length=255, verbose_name='Role')

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role


class Funcao(models.Model):
    nome_funcao = models.CharField(max_length=255, verbose_name='Nome da Função')
    roles = models.ManyToManyField(Role, blank=True, verbose_name='Roles da Função')

    class Meta:
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'

    def __str__(self):
        return self.nome_funcao


class Cargo(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Cargo")
    orgao_id = models.ForeignKey(Orgao, on_delete=models.CASCADE, verbose_name="Órgão", related_name="cargos")

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return f"{self.nome} - {self.orgao_id.orgao}"


class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, verbose_name="CPF", unique=True)
    matricula = models.CharField(max_length=50, verbose_name="Matrícula")
    numero_ordem = models.CharField(max_length=50, verbose_name="Nº de Ordem", blank=True, null=True)
    nome_guerra = models.CharField(max_length=100, verbose_name="Nome de Guerra")
    foto = models.ImageField(upload_to="fotos_usuarios/", verbose_name="Foto", blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cargo", help_text="Vínculo administrativo. Ex: 3º Sargento, Agente Administrativo")

    
    orgao_id = models.ForeignKey(Orgao, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Órgão")
    roles = models.ManyToManyField(Role, blank=True, verbose_name="Roles Pessoais Extras")
    
    funcao = models.ForeignKey(Funcao, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Função", related_name="usuarios")

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.nome_completo or self.username

    @property
    def get_all_roles(self):
        # Unifica as roles listadas na função que ele ocupa com as roles atribuídas manualmente ao seu perfil
        roles_funcao = self.funcao.roles.all() if self.funcao else Role.objects.none()
        roles_extras = self.roles.all()
        return roles_funcao | roles_extras
