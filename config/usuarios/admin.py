from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Orgao, Role, Funcao, Cargo, Usuario

@admin.register(Orgao)
class OrgaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'orgao')
    search_fields = ('orgao',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')
    search_fields = ('role',)


@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_funcao')
    search_fields = ('nome_funcao',)
    filter_horizontal = ('roles',)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'orgao_id')
    search_fields = ('nome',)
    list_filter = ('orgao_id',)


@admin.register(Usuario)
class UsuarioCustomAdmin(UserAdmin):
    list_display = ('username', 'nome_completo', 'cpf', 'matricula', 'cargo', 'orgao_id')
    search_fields = ('username', 'nome_completo', 'cpf', 'matricula', 'nome_guerra')
    list_filter = ('orgao_id', 'roles', 'is_staff', 'is_active')
    filter_horizontal = ('groups', 'user_permissions', 'roles')
    
    # Adicionando os campos customizados aos painéis nativos de User do Django
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Funcionais do GFrota', {
            'fields': (
                'nome_completo', 'cpf', 'matricula', 'numero_ordem', 
                'nome_guerra', 'foto', 'cargo', 'orgao_id', 'funcao', 'roles'
            )
        }),
    )
