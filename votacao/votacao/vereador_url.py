# -*- coding: utf-8 -*-

from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.VotacaoIndex.as_view(), name='votacao-index'),
]	
