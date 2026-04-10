from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import CreateApresentacaoView, ListApresentacaoView

app_name = 'operacional'

urlpatterns = [
    path('', ListApresentacaoView.as_view(), name='listar_apresentacoes'),
    path('cadastro_apresentacao/', CreateApresentacaoView.as_view(), name='cadastro_apresentacao'),
]
