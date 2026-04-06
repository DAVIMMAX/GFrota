from django.urls import path
from .views import UsuarioCreateView, UsuarioListView, UsuarioUpdateView

app_name = 'usuarios'

urlpatterns = [
    path('lista/', UsuarioListView.as_view(), name='lista'),
    path('cadastro/', UsuarioCreateView.as_view(), name='cadastro'),
    path('edicao/<int:pk>/', UsuarioUpdateView.as_view(), name='edicao'),
]
