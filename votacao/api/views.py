# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from datetime import datetime
from django.http import JsonResponse
from django.conf import settings

from votacao.votacao.forms import JSONVotacaoForm
from votacao.votacao.models import Votacao, Voto, Restricao

import json
import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from consumer.lib.views import SPLReuniaoComissaoView
from consumer.lib.msconsumer import MSCMCConsumer


# -----------------------------------------------------------------------------------
# chamada API para abrir um projeto para votação
# -----------------------------------------------------------------------------------
def abre_votacao(request, pac_id, par_id, codigo_projeto):
	response = JsonResponse({'status':'false','message':'Erro ao tentar abrir projeto para votação'}, status=404)

	if request.method == 'POST':

		widget_json = {}
		if (par_id != None):
			try:
				votacao = Votacao.objects.get(par_id=par_id)
				votacao.status = 'A'
				votacao.save()
			except Votacao.DoesNotExist:
				votacao = Votacao.objects.create(pac_id=pac_id, par_id=par_id, codigo_proposicao=codigo_projeto, status='A')
			response = JsonResponse({'status':'true','message':'Projeto foi aberto para votação'}, status=200)
	return response

# -----------------------------------------------------------------------------------
# chamada API para verificar se existe algum projeto aberto
# -----------------------------------------------------------------------------------
def verifica_abertos(request):
	response = JsonResponse({'status':'false','message':'Já existe projeto para votação aberto'}, status=200)

	abertas = Votacao.objects.filter(status='A')
	if abertas.count() <= 0:
		response = JsonResponse({'status':'true','message':'Nenhum projeto aberto para votação'}, status=200)
	return response

# -----------------------------------------------------------------------------------
# chamada API para retornar status do projeto
# -----------------------------------------------------------------------------------
def consome_projetos(request, pac_id):

	array_json=[]
	if (pac_id != None):
		search_url = '{}/api/spl/projetos_reuniao/{}/'.format(settings.MSCMC_SERVER, pac_id)
		r = requests.get(search_url, verify=False)
		projetos = r.json()
		for projeto in projetos:
			array_json.append(formata_projeto(projeto))
	return JsonResponse(array_json, safe=False)		

# -----------------------------------------------------------------------------------
# método auxiliar para formatação dos projetos
# -----------------------------------------------------------------------------------
def formata_projeto(projeto):
	ejson = {}
	try:
		votacao = Votacao.objects.get(par_id=projeto['par_id'])
		ejson['status'] = votacao.status
	except Votacao.DoesNotExist:
		ejson['status'] = 'F'
	ejson['pac_id'] = projeto['pac_id']
	ejson['par_id'] = projeto['par_id']
	ejson['iniciativa'] = projeto['iniciativa']
	ejson['relator'] = projeto['relator']
	ejson['conclusao_relator'] = projeto['conclusao_relator']
	ejson['conclusao_comissao'] = projeto['conclusao_comissao']
	ejson['tem_emendas'] = projeto['tem_emendas']
	ejson['sumula'] = projeto['sumula']
	ejson['codigo_proposicao'] = projeto['codigo_proposicao']
	return ejson

# -----------------------------------------------------------------------------------
# chamada API para fechar um projeto para votação
# -----------------------------------------------------------------------------------
def fecha_votacao(request, pac_id, par_id, codigo_projeto):
	response = JsonResponse({'status':'false','message':'Erro ao tentar fechar projeto para votação'}, status=404)

	if request.method == 'POST':
		widget_json = {}
		if (par_id != None):
			votacao = Votacao.objects.get(par_id=par_id)
			votacao.status = 'V'
			votacao.save()
			response = JsonResponse({'status':'true','message':'Projeto foi aberto para votação'}, status=200)
	return response	

# -----------------------------------------------------------------------------------
# chamada API para retornar projetos abertos para votação
# -----------------------------------------------------------------------------------
def retorna_aberto(request):

	result_json = []
	ejson = {}
	try:
		projeto = Votacao.objects.filter(status='A')[0]
	except IndexError:
		projeto = None
	if projeto:
		search_url = '{}/api/spl/projeto_reuniao/{}/{}/'.format(settings.MSCMC_SERVER, projeto.pac_id, projeto.par_id)
		id_projeto = projeto.id
		try:
			voto = Voto.objects.get(votacao=projeto, vereador=request.user)
			votado = True
			tipo_voto = voto.voto
		except Voto.DoesNotExist:
			votado = False
			tipo_voto = None
		r = requests.get(search_url, verify=False)

		projeto = r.json()
		try :
			ejson['id'] = id_projeto
			ejson['pac_id'] = projeto[0]['pac_id']
			ejson['par_id'] = projeto[0]['par_id']
			ejson['iniciativa'] = projeto[0]['iniciativa']
			ejson['relator'] = projeto[0]['relator']
			ejson['conclusao_relator'] = projeto[0]['conclusao_relator']
			ejson['conclusao_comissao'] = projeto[0]['conclusao_comissao']
			ejson['tem_emendas'] = projeto[0]['tem_emendas']
			ejson['sumula'] = projeto[0]['sumula']
			ejson['codigo_proposicao'] = projeto[0]['codigo_proposicao']
			ejson['votado'] = votado
			ejson['tipo_voto'] = tipo_voto
			result_json.append(ejson)
		except:
			pass
	return JsonResponse(result_json, safe=False)

# -----------------------------------------------------------------------------------
# chamada API para votar um projeto
# -----------------------------------------------------------------------------------
def vota(request, tipo_voto):
	response = JsonResponse({'status':'false','message':'Erro ao tentar votar.'}, status=404)

	if request.method == 'POST':
		widget_json = {}
		votacao = request.POST['votacao']
		if (votacao != None):
			try:
				votacao = Votacao.objects.get(id=votacao)
				voto = Voto.objects.create(votacao=votacao, vereador=request.user, voto=tipo_voto)
			except Votacao.DoesNotExist:
				response = JsonResponse({'status':'false','message':'Erro ao tentar votar.'}, status=404)
				return response
			response = JsonResponse({'status':'true','message':'Votação efetuada com sucesso', 'tipo_voto': tipo_voto}, status=200)
	return response	

# -----------------------------------------------------------------------------------
# chamada API para votar um projeto com restrição
# -----------------------------------------------------------------------------------
def vota_restricao(request, tipo_voto, restricao):
	response = JsonResponse({'status':'false','message':'Erro ao tentar votar.'}, status=404)

	if request.method == 'POST':
		widget_json = {}
		votacao = request.POST['votacao']
		if (votacao != None):
			try:
				votacao = Votacao.objects.get(id=votacao)
				voto = Voto.objects.create(votacao=votacao, vereador=request.user, voto=tipo_voto)
				restricao = Restricao.objects.create(voto=voto, restricao=restricao)
			except Votacao.DoesNotExist:
				response = JsonResponse({'status':'false','message':'Erro ao tentar votar.'}, status=404)
				return response
			response = JsonResponse({'status':'true','message':'Votação efetuada com sucesso', 'tipo_voto': restricao}, status=200)
	return response	

# -----------------------------------------------------------------------------------
# chamada API reunioes comissao
# -----------------------------------------------------------------------------------
class ConsomeReuniaoComissao(SPLReuniaoComissaoView):
	pass

# -----------------------------------------------------------------------------------
# chamada API para consumir reuniões dentro range datas
# -----------------------------------------------------------------------------------
def consome_reunioes_range(request, data_inicio, data_fim):
	consumer = MSCMCConsumer()
	return consumer.consome_reuniao_comissao_range(request, data_inicio, data_fim)