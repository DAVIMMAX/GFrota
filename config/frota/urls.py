from frota.views import ListViaturaView
from django.urls import path
from .views import CreateViaturaView, EditViaturaView, DeleteViaturaView
from django.views.generic import TemplateView

app_name = 'frota'

urlpatterns = [
    path('', ListViaturaView.as_view(), name='listar_viaturas'),
    path('cadastrar/', CreateViaturaView.as_view(), name='cadastrar_viatura'),
    path('dashboard/', TemplateView.as_view(template_name='frota/dashboard_frota.html'), name='dashboard'),
    path('editar/<int:pk>/', EditViaturaView.as_view(), name='editar_viatura'),
    path('deletar/<int:pk>/', DeleteViaturaView.as_view(), name='deletar_viatura'),   
]

