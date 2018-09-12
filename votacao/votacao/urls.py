# -*- coding: utf-8 -*-

from django.urls import include, path
from . import views

urlpatterns = [
	path('', views.AdminIndex.as_view(), name='index'),
	path('liberacao/', views.LiberacaoIndex.as_view(), name='liberacao-index'),
	path('votacao/', views.VotacaoIndex.as_view(), name='votacao-index'),
]	
