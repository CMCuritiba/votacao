# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from braces import views
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import requests, logging, functools

from autentica.util.mixin import CMCLoginRequired, CMCAdminLoginRequired
#from ..core.models import SetorChamado, Chamado

#----------------------------------------------------------------------------------------------
# Autenticador de acesso. Apenas vereadores.
#----------------------------------------------------------------------------------------------
class CMCVereadorLoginRequired(CMCLoginRequired):
	message_url = '/autentica/loga'

	def dispatch(self, request, *args, **kwargs):

		retorno = super(CMCLoginRequired, self).dispatch(request, *args, **kwargs)
		if retorno.status_code == 302:
			return HttpResponseRedirect(retorno.url)

		if (request.user.cpf != None):
			search_url = '{}/api/funcionario_cpf/{}/'.format(settings.MSCMC_SERVER, request.user.cpf)
			r = requests.get(search_url, verify=False)
			pessoa = r.json()
			try:
				# ind_estagiario == 0 (Vereador)
				# ind_estagiario == 2 (Efetivo)
				#if (pessoa['ind_estagiario'] != '0'):
				if (pessoa['ind_estagiario'] != 0 and pessoa['ind_estagiario'] != 2):
					return HttpResponseRedirect(self.message_url)
			except:
				return HttpResponseRedirect(self.message_url)
		return retorno