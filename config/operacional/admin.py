from django.contrib import admin
from .models import Apresentacao, Voo, Ocorrencia, AtribuicaoDoServico, ApresentacaoAtribuicao

@admin.register(Apresentacao)
class ApresentacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'turno', 'horario_inicial', 'horario_final', 'viatura_id', 'aeronave_id')
    list_filter = ('turno', 'horario_inicial')
    filter_horizontal = ('usuarios',)


@admin.register(Voo)
class VooAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'hora', 'destino', 'aeronave_id', 'apresentacao_id')
    list_filter = ('data', 'hora')


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_ocorrencia', 'data_ocorrencia', 'hora_ocorrencia')
    list_filter = ('data_ocorrencia', 'hora_ocorrencia')
    filter_horizontal = ('guarnicoes_id',)

@admin.register(ApresentacaoAtribuicao)
class ApresentacaoAtribuicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'apresentacao_id', 'atribuicao_id', 'usuario_id')
    list_filter = ('apresentacao_id', 'atribuicao_id', 'usuario_id')


@admin.register(AtribuicaoDoServico)
class AtribuicaoDoServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'atribuicao')
    list_filter = ('atribuicao',)
