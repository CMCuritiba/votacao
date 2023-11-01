# -*- coding: utf-8 -*-

from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from . import views
from consumer.lib.views import SPLReuniaoComissaoView

#router = routers.DefaultRouter()
#router.register(r'get_fake_calendario', views.FakeCalendarioViewSet, base_name='get_fake_calendario')


urlpatterns = [
	path('abre_votacao/<int:pac_id>/<int:par_id>/<codigo_projeto>/', views.abre_votacao, name='abre-votacao'),
	path('fecha_votacao/<int:pac_id>/<int:par_id>/<codigo_projeto>/', views.fecha_votacao, name='fecha-votacao'),
	path('verifica_abertos/', views.verifica_abertos, name='verifica-abertos'),
	path('retorna_aberto/', views.retorna_aberto, name='retorna_aberto'),
	path('consome_projetos/<int:pac_id>/', views.consome_projetos, name='consome-projetos'),
	path('vota/<tipo_voto>/', views.vota, name='vota'),
	path('vota_restricao/<tipo_voto>/<restricao>/', views.vota_restricao, name='vota-restricao'),
	path('consome_reuniao_comissao/', views.ConsomeReuniaoComissao.as_view(), name='consome-reuniao-comissao'),
	path('consome_reuniao_comissao_range/<data_inicio>/<data_fim>/', views.consome_reunioes_range, name='consome-reuniao-comissao-range'),
	path('relatorio_votacao/<int:pac_id>/', views.relatorio_votacao, name='relatorio-votacao'),
	path('textos_conclusao/<pro_codigo>/', views.consome_textos_conclusao, name='textos-conclusao'),
	path('vota_contrario/<tipo_voto>/<id_texto>/<tcp_nome>/<vereador>/', views.vota_contrario, name='vota-contrario'),
	path('vota_contrario_texto/<tipo_voto>/<texto_contrario>/', views.vota_contrario_texto, name='vota-contrario-texto'),
	path('reinicia_votacao/', views.reinicia_votacao, name='reinicia-votacao'),
	path('monta_painel/<int:pac_id>/<int:par_id>/<codigo_projeto>/', views.monta_painel, name='monta_painel'),
	path('usuarios/', views.usuarios, name='usuarios'),
]

#urlpatterns += router.urls
