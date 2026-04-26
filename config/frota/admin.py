from django.contrib import admin
from .models import StatusViatura, TipoRadio, Viatura, Radio, Aeronave, TipoAeronave

@admin.register(StatusViatura)
class StatusViaturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    search_fields = ('status',)


@admin.register(TipoRadio)
class TipoRadioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
    search_fields = ('tipo',)


@admin.register(Viatura)
class ViaturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'prefixo', 'placa', 'modelo', 'status_viatura_id')
    search_fields = ('prefixo', 'placa', 'modelo')
    list_filter = ('status_viatura_id',)


@admin.register(Radio)
class RadioAdmin(admin.ModelAdmin):
    list_display = ('id', 'prefixo', 'tipo_radio_id')
    search_fields = ('prefixo',)
    list_filter = ('tipo_radio_id',)

@admin.register(TipoAeronave)
class TipoAeronaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
    search_fields = ('tipo',)

@admin.register(Aeronave)
class AeronaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'prefixo',  'radio_id', 'tipo_aeronave_id')
    search_fields = ('nome', 'prefixo')
    list_filter = ('tipo_aeronave_id',)