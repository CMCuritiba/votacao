# -*- coding: utf-8 -*-
import json 

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
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from easy_pdf.views import PDFTemplateView

from autentica.util.mixin import CMCLoginRequired, CMCAdminLoginRequired
from cmcreport.lib.views import CMCReportView

from votacao.votacao.api.autenticacao import CMCVereadorLoginRequired
from votacao.votacao.forms import RelatorioVotacaoForm, FechaVotacoesForm
from votacao.votacao.models import Votacao, Voto, Restricao
from votacao.api.views import relatorio_votacao
from votacao.cron.jobs import fecha_votacoes

import logging

logger = logging.getLogger(__name__)

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

#--------------------------------------------------------------------------------------
# Relatorio Votacao impressao
#--------------------------------------------------------------------------------------        
class RelatorioVotacao(CMCReportView):
	template_name = 'admin/relatorio/votacao/relatorio.html'
	download_filename = 'relatorio_votacao.pdf'
	pac_id = None
	votacoes = []

	def get_context_data(self, **kwargs):
		context = super(CMCReportView, self).get_context_data(**kwargs)
		context['title'] = 'Relatório de Votação'
		context['pagesize'] = 'A4 portrait'
		context['votacoes'] = self.votacoes
		return context

	def post(self, request, *args, **kwargs):
		context = super(CMCReportView, self).get_context_data(**kwargs)
		form = RelatorioVotacaoForm(data = request.POST)
		if form.is_valid():
			self.pac_id = form['pac_id'].value()
			self.votacoes = relatorio_votacao(request, self.pac_id)

		return super(RelatorioVotacao, self).get(request, *args, **kwargs)	

#--------------------------------------------------------------------------------------
# Fecha Votações Abertas Index
#--------------------------------------------------------------------------------------    
class FechaTodasAbertasIndex(CMCAdminLoginRequired, SuccessMessageMixin, TemplateView):
    template_name = 'admin/fecha/index.html'                			

#--------------------------------------------------------------------------------------
# Fecha Votações Abertas
#--------------------------------------------------------------------------------------    
def fecha_abertas(request):
	logger.info("Fechamento forçado de votações abertas feito por %s", request.user.username)
	if request.method == 'POST':
		form = FechaVotacoesForm(request, request.POST)
		if form.is_valid():
			fecha_votacoes()
			return render(request, 'admin/fecha/sucesso.html')
		else:
			return render(request, 'admin/fecha/index.html')

#--------------------------------------------------------------------------------------
# Painel Votacao Index
#--------------------------------------------------------------------------------------    
class PainelIndex(CMCAdminLoginRequired, SuccessMessageMixin, TemplateView):
    template_name = 'admin/painel/index.html'