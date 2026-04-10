from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UsuarioCreationForm, UsuarioChangeForm
from .models import Usuario

class UsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'usuarios/cadastro_usuario.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.is_cadastrador
        return False

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuarios/lista_usuarios.html'
    context_object_name = 'usuarios'

class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    form_class = UsuarioChangeForm
    template_name = 'usuarios/edicao_usuario.html'
    success_url = reverse_lazy('usuarios:lista')

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.is_cadastrador
        return False

class UsuarioHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'usuarios/home.html'

    def test_func(self):
        usuario_logado = self.request.user
        if usuario_logado.is_authenticated:
            return usuario_logado.is_cadastrador
        return False

class UsuarioProfileView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'usuarios/profile.html'