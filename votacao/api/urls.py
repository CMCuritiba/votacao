# -*- coding: utf-8 -*-

from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from . import views

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
	path('consome_reuniao_comissao/', views.consome_reuniao_comissao, name='consome-reuniao-comissao'),
]	

#urlpatterns += router.urls
