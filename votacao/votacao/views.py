# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, DetailView
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse

from autentica.util.mixin import CMCLoginRequired, CMCAdminLoginRequired
from votacao.votacao.api.autenticacao import CMCVereadorLoginRequired

#--------------------------------------------------------------------------------------
# Admin Index
#--------------------------------------------------------------------------------------    
class AdminIndex(CMCAdminLoginRequired, SuccessMessageMixin, TemplateView):
    template_name = 'admin/index.html'    

#--------------------------------------------------------------------------------------
# Liberacao Index
#--------------------------------------------------------------------------------------    
class LiberacaoIndex(CMCAdminLoginRequired, SuccessMessageMixin, TemplateView):
    template_name = 'admin/liberacao/index.html'        

#--------------------------------------------------------------------------------------
# Votacao Index
#--------------------------------------------------------------------------------------    
class VotacaoIndex(CMCVereadorLoginRequired, SuccessMessageMixin, TemplateView):
    template_name = 'votacao/index.html'            

#--------------------------------------------------------------------------------------
# Relatorio Votacao Index
#--------------------------------------------------------------------------------------    
class RelatorioVotacaoIndex(CMCAdminLoginRequired, SuccessMessageMixin, TemplateView):
    template_name = 'admin/relatorio/votacao/index.html'                