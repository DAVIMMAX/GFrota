from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Apresentacao
from .forms import ApresentacaoCreationForm

class CreateApresentacaoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Apresentacao
    form_class = ApresentacaoCreationForm
    template_name = 'operacional/cadastro_apresentacao.html'
    success_url = reverse_lazy('operacional:listar_apresentacoes')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(role__iexact='cadastrador').exists()
        return False

class ListApresentacaoView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Apresentacao
    template_name = 'operacional/lista_apresentacoes.html'
    context_object_name = 'apresentacoes'

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(role__iexact='cadastrador').exists()
        return False
