from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import (
    CreateApresentacaoView, ListApresentacaoView, ListApresentacaoAtivaView, 
    AtribuirRadiosView, ApresentacaoAtribuicaoView, LocalizarRadioApresentacaoView, 
    ApresentacaoUpdateView, ApresentacaoRadioUpdateView, ApresentacaoDetailView, 
    OcorrenciaCreateView, OcorrenciaDeleteView, OcorrenciaDetailView, 
    OcorrenciaUpdateView, OcorrenciaListView
)

app_name = 'operacional'

urlpatterns = [
    path('', ListApresentacaoView.as_view(), name='listar_apresentacoes'),
    path('ativas/', ListApresentacaoAtivaView.as_view(), name='listar_apresentacoes_ativas'),
    path('cadastro_apresentacao/', CreateApresentacaoView.as_view(), name='cadastro_apresentacao'),
    path('listar_apresentacoes/', ListApresentacaoView.as_view(), name='listar_apresentacoes_todas'),
    path('listar_apresentacoes_ativas/', ListApresentacaoAtivaView.as_view(), name='listar_apresentacoes_ativas'),
    path('apresentacao/<int:apresentacao_id>/atribuir_radios/', AtribuirRadiosView.as_view(), name='atribuir_radios'),
    path('apresentacao/<int:apresentacao_id>/atribuicao/', ApresentacaoAtribuicaoView.as_view(), name='atribuicao_apresentacao'),
    path('localizar_radio_apresentacao/', LocalizarRadioApresentacaoView.as_view(), name='localizar_radio_apresentacao'),
    path('localizar_radio/', LocalizarRadioApresentacaoView.as_view(), name='localizar_radio'),
    path('apresentacao/<int:pk>/editar/', ApresentacaoUpdateView.as_view(), name='editar_apresentacao'),
    path('apresentacao_radio/<int:pk>/editar/', ApresentacaoRadioUpdateView.as_view(), name='editar_apresentacao_radio'),
    path('apresentacao/<int:pk>/', ApresentacaoDetailView.as_view(), name='perfil_apresentacao'),
    path('cadastro_ocorrencia/', OcorrenciaCreateView.as_view(), name='cadastro_ocorrencia'),
    path('listar_ocorrencias/', OcorrenciaListView.as_view(), name='listar_ocorrencias'),
    path('ocorrencia/<int:pk>/', OcorrenciaDetailView.as_view(), name='perfil_ocorrencia'),
    path('ocorrencia/<int:pk>/editar/', OcorrenciaUpdateView.as_view(), name='editar_ocorrencia'),
    path('ocorrencia/<int:pk>/excluir/', OcorrenciaDeleteView.as_view(), name='excluir_ocorrencia'),

]
