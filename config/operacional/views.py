from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from .models import Apresentacao, ApresentacaoRadio, Ocorrencia, AtribuicaoDoServico, ApresentacaoAtribuicao
from frota.models import Radio
from .forms import (
 ApresentacaoCreationForm, ApresentacaoRadioCreationForm, ApresentacaoUpdateForm, 
 OcorrenciaCreationForm,  ApresentacaoAtribuicaoForm
)
# Classes de Apresentação Geral
class CreateApresentacaoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Apresentacao
    form_class = ApresentacaoCreationForm
    template_name = 'operacional/cadastro_apresentacao.html'

    def get_success_url(self):
        return reverse_lazy('operacional:atribuicao_apresentacao', kwargs={'apresentacao_id': self.object.id})

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class ApresentacaoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Apresentacao
    template_name = 'operacional/profile_apresentacao.html'
    context_object_name = 'apresentacao'

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class ListApresentacaoView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Apresentacao
    context_object_name = 'apresentacoes'
    template_name = 'operacional/lista_apresentacoes.html'

    def get_queryset(self):
        return Apresentacao.objects.all().prefetch_related(
            'apresentacaoradio_set__radio_id', 
            'usuarios'
        ).order_by('-horario_inicial')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class ListApresentacaoAtivaView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Apresentacao
    ordering = ['-horario_inicial']
    template_name = 'operacional/lista_apresentacoes_ativas.html'
    context_object_name = 'apresentacoes_ativas'

    def get_queryset(self):
        return Apresentacao.objects.filter(
            horario_final__gt=timezone.now()
        ).prefetch_related(
            'apresentacaoradio_set__radio_id', 
            'usuarios'
        ).order_by('-horario_inicial')
    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False


class ApresentacaoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Apresentacao
    form_class  = ApresentacaoUpdateForm
    template_name = 'operacional/cadastro_apresentacao.html'
    success_url = reverse_lazy('operacional:listar_apresentacoes')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class ApresentacaoAtivaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Apresentacao
    form_class = ApresentacaoUpdateForm
    template_name = 'operacional/cadastro_apresentacao.html'
    success_url = reverse_lazy('operacional:listar_apresentacoes_ativas')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__in=['cadastrador', 'operador']).exists()
        return False

class ApresentacaoAtribuicaoView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'operacional/cadastro_atribuicao_apresentacao.html'
    success_url = reverse_lazy('operacional:listar_apresentacoes_ativas')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.get_all_roles.filter(nome__iexact='cadastrador').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apresentacao = Apresentacao.objects.prefetch_related('usuarios').get(id=self.kwargs['apresentacao_id'])
        
        # Mapeamento de atribuições atuais: {usuario_id: atribuicao_id}
        atribuicoes_atuais = {
            aa.usuario_id_id: aa.atribuicao_id_id 
            for aa in apresentacao.apresentacaoatribuicao_set.all()
        }
        
        # Preparar lista de usuários com seus papéis atuais
        usuarios_da_guarnicao = []
        for usuario in apresentacao.usuarios.all():
            usuario.current_atribuicao_id = atribuicoes_atuais.get(usuario.id)
            usuarios_da_guarnicao.append(usuario)
        
        context['apresentacao'] = apresentacao
        context['usuarios'] = usuarios_da_guarnicao
        context['atribuicoes'] = AtribuicaoDoServico.objects.all().order_by('atribuicao')
        return context

    def post(self, request, *args, **kwargs):
        apresentacao = Apresentacao.objects.get(id=self.kwargs['apresentacao_id'])
        for usuario in apresentacao.usuarios.all():
            atribuicao_id = request.POST.get(f'atribuicao_user_{usuario.id}')
            if atribuicao_id:
                ApresentacaoAtribuicao.objects.update_or_create(
                    usuario_id=usuario,
                    apresentacao_id=apresentacao,
                    defaults={'atribuicao_id_id': atribuicao_id}
                )
            else:
                # Se o usuário ficou sem atribuição
                ApresentacaoAtribuicao.objects.filter(
                    usuario_id=usuario, 
                    apresentacao_id=apresentacao
                ).delete()
        
        # Redirecionamento dinâmico baseado na origem
        next_path = request.GET.get('next')
        if next_path == 'ativas':
            return redirect('operacional:listar_apresentacoes_ativas')
        
        # Fluxo padrão (cadastro): Segue para atribuir rádios
        return redirect('operacional:atribuir_radios', apresentacao_id=apresentacao.id)

#--------------------------------------------------------------------------------------------------------#
# Classes de Rádio
class CreateApresentacaoRadioView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ApresentacaoRadio
    form_class = ApresentacaoRadioCreationForm
    template_name = 'operacional/cadastro_apresentacao_radio.html'
    success_url = reverse_lazy('operacional:listar_apresentacoes_ativas')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class AtribuirRadiosView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'operacional/atribuir_radios.html'
    success_url = reverse_lazy('operacional:listar_apresentacoes_ativas')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.get_all_roles.filter(nome__iexact='cadastrador').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apresentacao = Apresentacao.objects.prefetch_related('usuarios').get(id=self.kwargs['apresentacao_id'])
        
        # Mapeamento de atribuições atuais: {usuario_id: radio_id}
        atribuicoes_atuais = {
            ar.usuario_id_id: ar.radio_id_id 
            for ar in apresentacao.apresentacaoradio_set.all()
        }
        
        # Preparar lista de usuários com seus rádios atuais
        usuarios_da_guarnicao = []
        for usuario in apresentacao.usuarios.all():
            # Atribui temporariamente o ID do rádio atual ao objeto do usuário para fácil acesso no template
            usuario.current_radio_id = atribuicoes_atuais.get(usuario.id)
            usuarios_da_guarnicao.append(usuario)
        
        context['apresentacao'] = apresentacao
        context['usuarios'] = usuarios_da_guarnicao
        context['radios'] = Radio.objects.all().order_by('prefixo')
        return context

    def post(self, request, *args, **kwargs):
        apresentacao = Apresentacao.objects.get(id=self.kwargs['apresentacao_id'])
        for usuario in apresentacao.usuarios.all():
            radio_id = request.POST.get(f'radio_user_{usuario.id}')
            if radio_id:
                ApresentacaoRadio.objects.update_or_create(
                    usuario_id=usuario,
                    apresentacao_id=apresentacao,
                    defaults={'radio_id_id': radio_id}
                )
            else:
                # Se o usuário limpou o rádio, removemos a atribuição
                ApresentacaoRadio.objects.filter(
                    usuario_id=usuario, 
                    apresentacao_id=apresentacao
                ).delete()
        
        return redirect(self.success_url)

class ApresentacaoRadioAtivosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ApresentacaoRadio
    template_name = 'operacional/lista_apresentacao_radio_ativos.html'
    context_object_name = 'apresentacao_radios'

    def get_queryset(self):
        return ApresentacaoRadio.objects.filter(
            apresentacao_id__horario_final__gt=timezone.now()
        ).prefetch_related('apresentacao_id', 'radio_id', 'usuario_id')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__in=['cadastrador', 'operador']).exists()
        return False

class ApresentacaoRadioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ApresentacaoRadio
    form_class = ApresentacaoRadioCreationForm
    template_name = 'operacional/cadastro_apresentacao_radio.html'
    success_url = reverse_lazy('operacional:listar_apresentacoes_ativas')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class LocalizarRadioApresentacaoView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'operacional/localizar_radio_apresentacao.html'

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__in=['cadastrador', 'operador']).exists()
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        
        if query:
            # Busca o rádio pelo prefixo (exato ou similar)
            radios = Radio.objects.filter(prefixo__icontains=query).order_by('prefixo')
            context['query'] = query
            context['radios_encontrados'] = radios
            
            # Se encontrar exatamente um rádio, já facilitamos a exibição
            if radios.count() == 1:
                radio = radios.first()
                context['radio_selecionado'] = radio
                context['ultimo_usuario'] = radio.ultimo_usuario
                context['ultima_apresentacao'] = radio.ultima_apresentacao
        return context
        
        
        


#--------------------------------------------------------------------------------------------------------#
# Classes de Ocorrência
class OcorrenciaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ocorrencia
    form_class = OcorrenciaCreationForm
    template_name = 'operacional/cadastro_ocorrencia.html'
    success_url = reverse_lazy('operacional:listar_ocorrencias')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class OcorrenciaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Ocorrencia
    ordering = ['-data_ocorrencia']
    template_name = 'operacional/lista_ocorrencia.html'
    context_object_name = 'ocorrencias'

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class OcorrenciaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Ocorrencia
    template_name = 'operacional/profile_ocorrencia.html'
    context_object_name = 'ocorrencia'

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class OcorrenciaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ocorrencia
    form_class = OcorrenciaCreationForm
    template_name = 'operacional/cadastro_ocorrencia.html'
    success_url = reverse_lazy('operacional:listar_ocorrencias')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False

class OcorrenciaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ocorrencia
    template_name = 'operacional/profile_ocorrencia.html'
    success_url = reverse_lazy('operacional:listar_ocorrencias')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(nome__iexact='cadastrador').exists()
        return False