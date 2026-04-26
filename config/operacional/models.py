from django.db import models
from django.conf import settings
from django.utils import timezone

class AtribuicaoDoServico(models.Model):
    atribuicao = models.CharField(max_length=255, verbose_name="Atribuição")
    
    class Meta:
        verbose_name = "Atribuição do Serviço"
        verbose_name_plural = "Atribuições do Serviço"

    def __str__(self):
        return self.atribuicao

class Apresentacao(models.Model):

    TIPO_APRESENTACAO = (
        ('viatura', 'Viatura'),
        ('aeronave', 'Aeronave'),
        ('solo', 'Solo')
    )

    tipo_apresentacao = models.CharField(max_length=50, choices=TIPO_APRESENTACAO, verbose_name="Tipo de Apresentação", default='viatura')
    viatura_id = models.ForeignKey('frota.Viatura', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Viatura")
    aeronave_id = models.ForeignKey('frota.Aeronave', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Aeronave")
    solo_id = models.ForeignKey('frota.Solo', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Solo")
    turno = models.CharField(max_length=50, verbose_name="Turno")
    horario_inicial = models.DateTimeField(verbose_name="Horário Inicial")
    horario_final = models.DateTimeField(verbose_name="Horário Final", default=timezone.now)
    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)

    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Usuários/Guarnição", related_name="apresentacoes")
    inserido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Inserido por")
    class Meta:
        verbose_name = "Apresentação"
        verbose_name_plural = "Apresentações"

    def __str__(self):
        return f"Apresentação {self.id} - Turno: {self.turno}"

    def is_ativa(self):
        return self.horario_final > timezone.now()

    @property
    def equipe_com_radios(self):
        """
        Retorna uma lista de dicionários contendo o usuário e seu rádio 
        nesta apresentação específica.
        """
        # Cria um dicionário para busca rápida de rádios por ID de usuário
        radios_mapeamento = {
            ar.usuario_id_id: ar.radio_id.prefixo 
            for ar in self.apresentacaoradio_set.all()
        }
        
        equipe = []
        for usuario in self.usuarios.all():
            equipe.append({
                'nome': usuario.nome_completo or usuario.username,
                'radio': radios_mapeamento.get(usuario.id)
            })
        return equipe

class ApresentacaoAtribuicao(models.Model):
    apresentacao_id = models.ForeignKey(Apresentacao, on_delete=models.CASCADE, verbose_name="Apresentação")
    atribuicao_id = models.ForeignKey(AtribuicaoDoServico, on_delete=models.CASCADE, verbose_name="Atribuição")
    usuario_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário")

    class Meta:
        verbose_name = "Atribuição da Apresentação"
        verbose_name_plural = "Atribuições da Apresentação"

    def __str__(self):
        return f"{self.usuario_id} - {self.atribuicao_id} ({self.apresentacao_id})"

class ApresentacaoRadio(models.Model):
    usuario_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário")
    radio_id = models.ForeignKey('frota.Radio', on_delete=models.CASCADE, verbose_name="Rádio")
    apresentacao_id = models.ForeignKey(Apresentacao, on_delete=models.CASCADE, verbose_name="Apresentação")

    class Meta:
        verbose_name = "Rádio da Apresentação"
        verbose_name_plural = "Rádios da Apresentação"
        unique_together = ('usuario_id', 'apresentacao_id')

    def __str__(self):
        return f"{self.usuario_id} - {self.radio_id} ({self.apresentacao_id})"
    
    @property
    def is_ativo(self):
        return self.apresentacao_id.is_ativa()
    


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
    guarnicoes_id = models.ManyToManyField(Apresentacao, verbose_name="Guarnição")
    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"

    def __str__(self):
        return f"Ocorrência: {self.tipo_ocorrencia}"


