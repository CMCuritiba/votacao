# -*- coding: utf-8 -*-

from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
	#path('', views.AdminIndex.as_view(), name='index'),
	path('liberacao/', views.LiberacaoIndex.as_view(), name='liberacao-index'),
	path('votacao/', views.VotacaoIndex.as_view(), name='votacao-index'),
	path('relatorio/votacao/', views.RelatorioVotacaoIndex.as_view(), name='relatorio-votacao'),
	path('relatorio/votacao/imprime/', views.RelatorioVotacao.as_view(), name='relatorio-votacao-imprime'),
	path('fecha/abertas/', views.FechaTodasAbertasIndex.as_view(), name='fecha-abertas-index'),
	path('fecha/abertas/fecha', views.fecha_abertas, name='fecha-abertas'),
	path('painel/', views.PainelIndex.as_view(), name='painel-index'),
	path('gerencia/usuario/', views.AdminUsuariosIndex.as_view(), name='usuario-index'),
	path('gerencia/usuario/altera/<int:pk>/', views.AdminUsuariosUpdate.as_view(), name='usuario-altera'),
]	
