# -*- coding: utf-8 -*-

from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
	# Teste INICIO
	# path('', views.VotacaoIndex.as_view(), name='votacao-index'),
	path('vota/', views.VotacaoIndex.as_view(), name='votacao-index'),
	# Teste FIM
]	
