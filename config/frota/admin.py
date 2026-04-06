from django.contrib import admin
from .models import StatusViatura, TipoRadio, Viatura, Radio, Aeronave

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


@admin.register(Aeronave)
class AeronaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'prefixo', 'recurso', 'radio_id')
    search_fields = ('prefixo', 'recurso')
