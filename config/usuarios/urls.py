from django.urls import path
from .views import UsuarioCreateView, UsuarioListView, UsuarioUpdateView, UsuarioHomeView, UsuarioProfileView

app_name = 'usuarios'

urlpatterns = [
    path('', UsuarioHomeView.as_view(), name='home'),
    path('usuarios/lista/', UsuarioListView.as_view(), name='lista'),
    path('usuarios/cadastro/', UsuarioCreateView.as_view(), name='cadastro'),
    path('usuarios/edicao/<int:pk>/', UsuarioUpdateView.as_view(), name='edicao'),
    path('usuarios/profile/<int:pk>/', UsuarioProfileView.as_view(), name='profile'),
]
