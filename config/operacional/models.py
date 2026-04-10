from django.db import models
from django.conf import settings

class Apresentacao(models.Model):

    TIPO_APRESENTACAO = (
        ('viatura', 'Viatura'),
        ('aeronave', 'Aeronave'),
    )

    tipo_apresentacao = models.CharField(max_length=50, choices=TIPO_APRESENTACAO, verbose_name="Tipo de Apresentação", default='viatura')
    viatura_id = models.ForeignKey('frota.Viatura', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Viatura")
    aeronave_id = models.ForeignKey('frota.Aeronave', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Aeronave")
    turno = models.CharField(max_length=50, verbose_name="Turno")
    horario_inicial = models.DateTimeField(verbose_name="Horário Inicial")
    horario_final = models.DateTimeField(null=True, blank=True, verbose_name="Horário Final")
    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)

    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Usuários/Guarnição", related_name="apresentacoes")
    inserido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Inserido por")
    class Meta:
        verbose_name = "Apresentação"
        verbose_name_plural = "Apresentações"

    def __str__(self):
        return f"Apresentação {self.id} - Turno: {self.turno}"


class Voo(models.Model):
    data = models.DateField(verbose_name="Data")
    hora = models.TimeField(verbose_name="Hora")
    destino = models.CharField(max_length=255, verbose_name="Destino")
    aeronave_id = models.ForeignKey('frota.Aeronave', on_delete=models.CASCADE, verbose_name="Aeronave")
    apresentacao_id = models.ForeignKey(Apresentacao, on_delete=models.CASCADE, verbose_name="Apresentação")
    hora_retorno = models.TimeField(null=True, blank=True, verbose_name="Hora de Retorno")

    class Meta:
        verbose_name = "Voo"
        verbose_name_plural = "Voos"

    def __str__(self):
        return f"Voo {self.id} - Destino: {self.destino}"


class Ocorrencia(models.Model):
    tipo_ocorrencia = models.CharField(max_length=255, verbose_name="Tipo de Ocorrência")
    data_ocorrencia = models.DateField(verbose_name="Data da Ocorrência")
    hora_ocorrencia = models.TimeField(verbose_name="Hora da Ocorrência")
    apresentacao_id = models.ForeignKey(Apresentacao, on_delete=models.CASCADE, verbose_name="Apresentação")
    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"

    def __str__(self):
        return f"Ocorrência: {self.tipo_ocorrencia}"
