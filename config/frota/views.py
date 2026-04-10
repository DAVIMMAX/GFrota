from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Viatura 
from .forms import ViaturaCreationForm, ViaturaChangeForm


class CreateViaturaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Viatura
    form_class = ViaturaCreationForm
    template_name = 'frota/cadastro_viatura.html'
    success_url = reverse_lazy('frota:listar_viaturas')

    def test_func(self):
        usuario_logado = self.request.user
        # Valida se o usuário tem a Role de 'admin' herdada da função ou salva manualmente
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(role__iexact='cadastrador').exists()
        return False

class ListViaturaView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Viatura
    template_name = 'frota/lista_viaturas.html'
    context_object_name = 'viaturas'

    def test_func(self):
        usuario_logado = self.request.user
        # Valida se o usuário tem a Role de 'admin' herdada da função ou salva manualmente
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(role__iexact='cadastrador').exists()
        return False

class EditViaturaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Viatura
    form_class = ViaturaChangeForm
    template_name = 'frota/editar_viatura.html'
    success_url = reverse_lazy('frota:listar_viaturas')

    def test_func(self):
        usuario_logado = self.request.user
        # Valida se o usuário tem a Role de 'admin' herdada da função ou salva manualmente
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(role__iexact='cadastrador').exists()
        return False

class DeleteViaturaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Viatura
    template_name = 'frota/deletar_viatura.html'
    success_url = reverse_lazy('frota:lista')

    def test_func(self):
        usuario_logado = self.request.user
        # Valida se o usuário tem a Role de 'admin' herdada da função ou salva manualmente
        if usuario_logado.is_authenticated:
            return usuario_logado.get_all_roles.filter(role__iexact='cadastrador').exists()
        return False    