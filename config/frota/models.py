from django.db import models

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


class Viatura(models.Model):
    placa = models.CharField(max_length=50, verbose_name="Placa")
    modelo = models.CharField(max_length=255, verbose_name="Modelo")
    prefixo = models.CharField(max_length=100, verbose_name="Prefixo")
    foto = models.ImageField(upload_to="fotos_viaturas/", verbose_name="Foto", blank=True, null=True)
    status_viatura_id = models.ForeignKey(StatusViatura, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Status da Viatura")

    class Meta:
        verbose_name = "Viatura"
        verbose_name_plural = "Viaturas"

    def __str__(self):
        return f"{self.prefixo} - {self.placa}"


class Radio(models.Model):
    prefixo = models.CharField(max_length=100, verbose_name="Prefixo")
    tipo_radio_id = models.ForeignKey(TipoRadio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Rádio")

    class Meta:
        verbose_name = "Rádio"
        verbose_name_plural = "Rádios"

    def __str__(self):
        return self.prefixo


class Aeronave(models.Model):
    prefixo = models.CharField(max_length=100, verbose_name="Prefixo")
    recurso = models.CharField(max_length=255, verbose_name="Recurso")
    radio_id = models.ForeignKey(Radio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rádio")

    class Meta:
        verbose_name = "Aeronave"
        verbose_name_plural = "Aeronaves"

    def __str__(self):
        return self.prefixo
