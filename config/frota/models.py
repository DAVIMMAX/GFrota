from django.db import models
from django.utils import timezone

class StatusViatura(models.Model):
    status = models.CharField(max_length=255, verbose_name='Status')

    class Meta:
        verbose_name = 'Status de Viatura'
        verbose_name_plural = 'Status de Viaturas'

    def __str__(self):
        return self.status


class TipoRadio(models.Model):
    tipo = models.CharField(max_length=255, verbose_name='Tipo')

    class Meta:
        verbose_name = 'Tipo de Rádio'
        verbose_name_plural = 'Tipos de Rádio'

    def __str__(self):
        return self.tipo

class TipoAeronave(models.Model):
    tipo = models.CharField(max_length=255, verbose_name='Tipo')

    class Meta:
        verbose_name = 'Tipo de Aeronave'
        verbose_name_plural = 'Tipos de Aeronaves'

    def __str__(self):
        return self.tipo

class Solo(models.Model):
    tipo = models.CharField(max_length=255, verbose_name='Tipo')
    
    class Meta:
        verbose_name = 'Solo'
        verbose_name_plural = 'Solos'

    def __str__(self):
        return self.tipo
    


class Viatura(models.Model):
    placa = models.CharField(max_length=50, verbose_name="Placa")
    marca = models.CharField(max_length=255, verbose_name="Marca", default='Viatura')
    modelo = models.CharField(max_length=255, verbose_name="Modelo", default='Viatura')
    prefixo = models.CharField(max_length=100, verbose_name="Prefixo")
    foto = models.ImageField(upload_to="fotos_viaturas/", verbose_name="Foto", blank=True, null=True)
    status_viatura_id = models.ForeignKey(StatusViatura, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Status da Viatura")

    class Meta:
        verbose_name = "Viatura"
        verbose_name_plural = "Viaturas"

    def __str__(self):
        return f"{self.prefixo} - {self.placa}"
    
    @property
    def is_ativo(self):
        return self.status_viatura_id.status == 'Ativo'
    
    @property
    def ultimo_registro(self):
        return self.apresentacaoviatura_set.order_by('-apresentacao_id__horario_inicial').first()
    
    @property
    def ultimo_usuario(self):
        return self.apresentacaoviatura_set.order_by('-apresentacao_id__horario_inicial').first().usuario_id
    
    @property
    def ultima_apresentacao(self):
        return self.apresentacaoviatura_set.order_by('-apresentacao_id__horario_inicial').first().apresentacao_id
    @property
    def return_foto(self):
        if self.foto:
            return self.foto.url
        else:
            return "/static/img/default_vehicle.png"

class Radio(models.Model):
    prefixo = models.CharField(max_length=100, verbose_name="Prefixo", unique=True)
    tipo_radio_id = models.ForeignKey(TipoRadio, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Tipo de Radio", default=None)

    class Meta:
        verbose_name = "Radio"
        verbose_name_plural = "Radios"

    def __str__(self):
        return self.prefixo

    @property
    def is_ativo(self):
        # Um rádio está ativo se houver uma apresentação vinculada a ele que ainda esteja ativa
        return self.apresentacaoradio_set.filter(apresentacao_id__horario_final__gt=timezone.now()).exists()

    @property
    def ultimo_usuario(self):
        # Retorna o último usuário que utilizou este rádio baseado no início da apresentação
        last_assignment = self.apresentacaoradio_set.order_by('-apresentacao_id__horario_inicial').first()
        if last_assignment:
            return last_assignment.usuario_id
        return None

    @property
    def ultima_apresentacao(self):
        # Retorna a última apresentação em que este rádio foi utilizado
        last_assignment = self.apresentacaoradio_set.order_by('-apresentacao_id__horario_inicial').first()
        if last_assignment:
            return last_assignment.apresentacao_id
        return None


class Aeronave(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome", default='Aeronave')
    prefixo = models.CharField(max_length=100, verbose_name="Prefixo")
    radio_id = models.ForeignKey(Radio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rádio")
    tipo_aeronave_id = models.ForeignKey(TipoAeronave, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Aeronave")
    
    class Meta:
        verbose_name = "Aeronave"
        verbose_name_plural = "Aeronaves"

    def __str__(self):
        return self.prefixo
