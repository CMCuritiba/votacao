# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from datetime import datetime
from django.http import JsonResponse
from django.conf import settings

from django.db import IntegrityError, transaction

from votacao.votacao.forms import JSONVotacaoForm
from votacao.votacao.models import Votacao, Voto, Restricao, VotoContrario, Restricao, VotoContrarioComplemento
from votacao.api.util.json_util import ReuniaoJSON, VotacaoJSON, VotoJSON, TotalJSON, JsonConvert, PainelVotacaoJSON
from votacao.api.util.db_util import verifica

import json
import requests

import jsonref

from consumer.lib.views import SPLReuniaoComissaoView
from consumer.lib.msconsumer import MSCMCConsumer
from consumer.lib.helper import ServiceHelper

from autentica.models import User as Usuario

import logging

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------------
# chamada API para abrir um projeto para votação
# -----------------------------------------------------------------------------------
def abre_votacao(request, pac_id, par_id, codigo_projeto):
    response = JsonResponse({'status':'false','message':'Erro ao tentar abrir projeto para votação'}, status=404)

    if request.method == 'POST':

        widget_json = {}
        if (par_id != None):
            #with transaction.atomic():
            if verifica('A'):
                try:
                    votacao = Votacao.objects.get(pac_id=pac_id, par_id=par_id, codigo_proposicao=codigo_projeto)
                    if votacao.status == 'F':
                        votacao.status = 'A'
                        votacao.save()
                        logger.info("Votação para projeto %s aberta por %s", codigo_projeto, request.user.username)
                    else:
                        logger.info("Tentativa de abrir projeto aberto ou já votado para projeto %s aberta por %s", codigo_projeto, request.user.username)
                except Votacao.DoesNotExist:
                    votacao = Votacao.objects.create(pac_id=pac_id, par_id=par_id, codigo_proposicao=codigo_projeto, status='A')
                    logger.info("Votação para projeto %s aberta por %s", codigo_projeto, request.user.username)
            response = JsonResponse({'status':'true','message':'Projeto foi aberto para votação'}, status=200)
    return response

# -----------------------------------------------------------------------------------
# chamada API para verificar se existe algum projeto aberto
# -----------------------------------------------------------------------------------
def verifica_abertos(request):
    response = JsonResponse({'status':'false','message':'Já existe projeto para votação aberto'}, status=200)

    if verifica('A'):
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
        #votacao = Votacao.objects.get(par_id=projeto['par_id'])
        votacao = Votacao.objects.get(pac_id=projeto['pac_id'], par_id=projeto['par_id'], codigo_proposicao=projeto['codigo_proposicao'])
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
    response = JsonResponse({'status':'false','message':'Erro ao tentar encerrar votação para o projeto'}, status=404)

    if request.method == 'POST':
        widget_json = {}
        if (par_id != None):
            votacao = Votacao.objects.get(pac_id=pac_id, par_id=par_id, codigo_proposicao=codigo_projeto)
            if votacao.status == 'A':
                votacao.status = 'V'
                votacao.save()
                logger.info("Votação para projeto %s encerrada por %s", codigo_projeto, request.user.username)
            else:
                logger.info("Tentativa fechar votação já encerrada para projeto %s encerrada por %s", codigo_projeto, request.user.username)
            response = JsonResponse({'status':'true','message':'Projeto com votação encerrada'}, status=200)
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
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        votacao = body['votacao']
        if (votacao != None):
            try:
                votacao = Votacao.objects.get(id=votacao)
                if votacao.status == 'A':
                    voto = Voto.objects.create(votacao=votacao, vereador=request.user, voto=tipo_voto)
                    if voto.voto == 'V':
                        logger.info("Pedido de vistas por %s", request.user.username)
                        Voto.objects.filter(votacao=votacao).exclude(voto='V').delete()
                        votacao.status = 'V'
                        votacao.save()
                        logger.info("Votação encerrada por pedido de vistas por %s", request.user.username)
                        response = JsonResponse({'status':'true','message':'Pedido de vistas', 'tipo_voto': tipo_voto}, status=200)
                    else:
                        logger.info("Voto %s por %s", tipo_voto, request.user.username)
                        response = JsonResponse({'status':'true','message':'Votação efetuada com sucesso', 'tipo_voto': tipo_voto}, status=200)
            except Votacao.DoesNotExist:
                response = JsonResponse({'status':'false','message':'Erro ao tentar votar.'}, status=404)
                return response
            except IntegrityError:
                response = JsonResponse({'status':'false','message':'Tentativa de votar mais de 1 vez.'}, status=404)
                logger.info("Tentativa de votar mais de uma vez por %s", request.user.username)
                return response                
    return response 

# -----------------------------------------------------------------------------------
# chamada API para votar um projeto com restrição
# -----------------------------------------------------------------------------------
def vota_restricao(request, tipo_voto, restricao):
    response = JsonResponse({'status':'false','message':'Erro ao tentar votar.'}, status=404)

    if request.method == 'POST':
        widget_json = {}
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        votacao = body['votacao']
        if (votacao != None):
            try:
                votacao = Votacao.objects.get(id=votacao)
                voto = Voto.objects.create(votacao=votacao, vereador=request.user, voto=tipo_voto)
                restricao = Restricao.objects.create(voto=voto, restricao=restricao)
                logger.info("Voto %s por %s", tipo_voto, request.user.username)
            except Votacao.DoesNotExist:
                response = JsonResponse({'status':'false','message':'Erro ao tentar votar.'}, status=404)
                return response
            except IntegrityError:
                response = JsonResponse({'status':'false','message':'Tentativa de votar mais de 1 vez.'}, status=404)
                logger.info("Tentativa de votar mais de uma vez por %s", request.user.username)
                return response                                
            response = JsonResponse({'status':'true','message':'Votação efetuada com sucesso', 'tipo_voto': restricao.voto.voto}, status=200)
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

# -----------------------------------------------------------------------------------
# chamada API para gerar dados relatório votação formato JSON
# -----------------------------------------------------------------------------------
def relatorio_votacao(request, pac_id):
    consumer = MSCMCConsumer()

    rec_id = consumer.consome_rec_id(request, pac_id)
    reuniao = consumer.consome_reuniao(request, rec_id)
    con_id = reuniao['con_id']
    rec_tipo_reuniao = reuniao['rec_tipo_reuniao']
    #print(reuniao)
    rec_data = reuniao['rec_data']
    rec_numero = reuniao['rec_numero']
    comissao = consumer.consome_comissao(request, con_id)
    ini_nome = comissao['ini_nome']
    reuniao_js = ReuniaoJSON(rec_id, rec_tipo_reuniao, rec_numero, ini_nome, rec_data)

    votacoes_model = Votacao.objects.filter(status='V', pac_id = pac_id)
    for votacao in votacoes_model:
        try:
            search_url = '{}/api/spl/projeto_reuniao/{}/{}/'.format(settings.MSCMC_SERVER, votacao.pac_id, votacao.par_id)
            r = requests.get(search_url, verify=False)
            projeto = r.json()
            relator = projeto[0]['relator']
            iniciativa = projeto[0]['iniciativa']
        except:
            relator = None
            iniciativa = None
        tot_favoravel = 0
        tot_favoravel_restricoes = 0
        tot_contrario = 0
        tot_abstencao = 0
        tot_vista = 0
        if rec_id is not None:
            votacao_incluir = VotacaoJSON(con_id, votacao.codigo_proposicao, relator, iniciativa)

        if rec_id is not None and con_id is not None:
            for voto in votacao.lista_votos():
                desc_restricao = ''
                if voto.voto == 'F':
                    tot_favoravel += 1
                elif voto.voto == 'C':
                    try: 
                        voto_contrario = VotoContrario.objects.get(voto_id=voto.id)
                        voto_contrario_complemento = VotoContrarioComplemento.objects.get(voto_contrario_id=voto_contrario.id)
                        desc_contrario = voto_contrario_complemento.vereador + " - " + voto_contrario_complemento.tcp_nome
                    except VotoContrario.DoesNotExist:
                            restricao = Restricao.objects.get(voto_id=voto.id)
                            desc_contrario = "COM RESTRIÇÕES - " + restricao.restricao
                    tot_contrario += 1
                elif voto.voto == 'R':
                    tot_favoravel_restricoes += 1
                    restricao = Restricao.objects.get(voto=voto)
                    desc_restricao = restricao.restricao
                elif voto.voto == 'A':
                    tot_abstencao += 1
                elif voto.voto == 'V':
                    tot_vista += 1
                # votacao_incluir.VotoJSONs.append(VotoJSON(voto.vereador.get_full_name(), voto.voto, desc_restricao))
                votacao_incluir.VotoJSONs.append(VotoJSON(voto.vereador.get_full_name(), voto.voto, '', desc_contrario))
            votacao_incluir.TotalJSONs.append(TotalJSON(tot_contrario, tot_favoravel, tot_favoravel_restricoes, tot_abstencao, tot_vista))
        reuniao_js.VotacaoJSONs.append(votacao_incluir)     

    asJson = JsonConvert.ToJSON(reuniao_js)
    fromJson = JsonConvert.FromJSON(asJson)
    asJsonFromJson = JsonConvert.ToJSON(fromJson)
    data = jsonref.loads(asJson)
    # print(data)
    return data

# -----------------------------------------------------------------------------------
# chamada API para consumir textos de conclusao
# -----------------------------------------------------------------------------------
def consome_textos_conclusao(request, pro_codigo):
    helper = ServiceHelper()
    return helper.get_textos_conclusao(pro_codigo)

# -----------------------------------------------------------------------------------
# chamada API para votar contrário
# -----------------------------------------------------------------------------------
def vota_contrario(request, tipo_voto, id_texto, tcp_nome, vereador):
    response = JsonResponse({'status':'false','message':'Erro ao tentar votar contrário.'}, status=404)

    if request.method == 'POST':
        widget_json = {}
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        votacao = body['votacao']
        if (votacao != None):
            try:
                votacao = Votacao.objects.get(id=votacao)
                voto = Voto.objects.create(votacao=votacao, vereador=request.user, voto=tipo_voto)
                contrario = VotoContrario.objects.create(voto=voto, id_texto=id_texto)
                complemento = VotoContrarioComplemento.objects.create(voto_contrario=contrario, tcp_nome=tcp_nome, vereador=vereador)
                logger.info("Voto %s por %s", tipo_voto, request.user.username)
            except Votacao.DoesNotExist:
                response = JsonResponse({'status':'false','message':'Erro ao tentar votar contrário.'}, status=404)
                return response
            response = JsonResponse({'status':'true','message':'Votação contrária efetuada com sucesso', 'tipo_voto': tipo_voto}, status=200)
    return response     
# -----------------------------------------------------------------------------------
# chamada API para votar contrário com texto
# -----------------------------------------------------------------------------------
def vota_contrario_texto(request, tipo_voto, texto_contrario):
    response = JsonResponse({'status':'false','message':'Erro ao tentar votar contrário.'}, status=404)

    if request.method == 'POST':
        widget_json = {}
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        votacao = body['votacao']
        if (votacao != None):
            try:
                votacao = Votacao.objects.get(id=votacao)
                voto = Voto.objects.create(votacao=votacao, vereador=request.user, voto=tipo_voto)
                restricao = Restricao.objects.create(voto=voto, restricao=texto_contrario)
                logger.info("Voto %s por %s", tipo_voto, request.user.username)
            except Votacao.DoesNotExist:
                response = JsonResponse({'status':'false','message':'Erro ao tentar votar contrário.'}, status=404)
                return response
            response = JsonResponse({'status':'true','message':'Votação contrária efetuada com sucesso', 'tipo_voto': tipo_voto}, status=200)
    return response     
# -----------------------------------------------------------------------------------
# chamada API para reiniciar votacao
# -----------------------------------------------------------------------------------
def reinicia_votacao(request):
    response = JsonResponse({'status':'false','message':'Erro ao tentar reiniciar votacao.'}, status=404)

    if request.method == 'POST':
        widget_json = {}
        pac_id = request.POST['pac_id']
        par_id = request.POST['par_id']
        codigo_proposicao = request.POST['codigo_proposicao']
        if (pac_id != None and par_id != None and codigo_proposicao != None):
            try:
                votacao = Votacao.objects.get(pac_id=pac_id, par_id=par_id, codigo_proposicao=codigo_proposicao)
                if votacao.status == 'V':
                    logger.info("Votação pac_id %s, par_id %s codigo_proposicao %s reiniciada por %s", pac_id, par_id, codigo_proposicao, request.user.username)
                    
                    votos = votacao.voto_set.all()
                    for voto in votos:
                        voto.votocontrario_set.all().delete()
                        voto.restricao_set.all().delete()
                    votos.delete()
                    votacao.status = 'A'
                    votacao.save()
                    response = JsonResponse({'status':'true','message':'Votação reiniciada com sucesso'}, status=200)
                else:
                    logger.info("Votação pac_id %s, par_id %s codigo_proposicao %s tentativa de reiniciar votação não fechada por %s", pac_id, par_id, codigo_proposicao, request.user.username)
            except Votacao.DoesNotExist:
                logger.info("Votação pac_id %s, par_id %s codigo_proposicao %s não encontrada para reiniciar por %s", pac_id, par_id, codigo_proposicao, request.user.username)
                response = JsonResponse({'status':'false','message':'Erro ao reiniciar votação.'}, status=404)
                return response
    return response     

# -----------------------------------------------------------------------------------
# chamada API para retornar status do projeto
# -----------------------------------------------------------------------------------
def monta_painel(request, pac_id, par_id, codigo_projeto):
    consumer = MSCMCConsumer()
    data = []

    print('--1')
    array_json=[]
    if (request.method == 'GET'):
        if (pac_id != None and par_id != None and codigo_projeto != None):
            tot_favoravel = 0
            tot_favoravel_restricoes = 0
            tot_contrario = 0
            tot_abstencao = 0
            tot_vista = 0
            try:
                print('--2')
                rec_id = consumer.consome_rec_id(request, pac_id)
                print('--3')
                reuniao = consumer.consome_reuniao(request, rec_id)
                print('--4')
                con_id = reuniao['con_id']
                rec_tipo_reuniao = reuniao['rec_tipo_reuniao']
                rec_data = reuniao['rec_data']
                rec_numero = reuniao['rec_numero']
                print('--5')
                comissao = consumer.consome_comissao(request, con_id)
                print('--6')
                ini_nome = comissao['ini_nome']

                search_url = '{}/api/spl/projeto/{}/{}/{}/'.format(settings.MSCMC_SERVER, pac_id, par_id, codigo_projeto)
                print('--7')
                r = requests.get(search_url, verify=False)
                print('--8')
                projeto = r.json()
                print('--9')
                codigo_proposicao = projeto[0]['codigo_proposicao']
                print('--10')
                iniciativa = projeto[0]['iniciativa']
                print('--11')
                sumula = projeto[0]['sumula']
                print('--12')
                relator = projeto[0]['relator']
                print('--13')
                conclusao = projeto[0]['conclusao_relator']
                print('--14')

                try:
                    votacao_banco = Votacao.objects.get(pac_id=pac_id, par_id=par_id, codigo_proposicao=codigo_projeto)
                    votacao = PainelVotacaoJSON(codigo_proposicao, relator, iniciativa, sumula, conclusao, votacao_banco.status, ini_nome)
                except Votacao.DoesNotExist:
                    votacao = PainelVotacaoJSON(codigo_proposicao, relator, iniciativa, sumula, conclusao, 'F', ini_nome)

                #votacao = PainelVotacaoJSON(codigo_proposicao, relator, iniciativa, sumula, conclusao, votacao_banco.status, ini_nome)

                for voto in votacao_banco.lista_votos():
                    desc_contrario = ''
                    if voto.voto == 'F':
                        tot_favoravel += 1
                    elif voto.voto == 'C':
                        try: 
                            voto_contrario = VotoContrario.objects.get(voto_id=voto.id)
                            voto_contrario_complemento = VotoContrarioComplemento.objects.get(voto_contrario_id=voto_contrario.id)
                            desc_contrario = voto_contrario_complemento.vereador + " - " + voto_contrario_complemento.tcp_nome
                        except VotoContrario.DoesNotExist:
                            restricao = Restricao.objects.get(voto_id=voto.id)
                            desc_contrario = "COM RESTRIÇÕES - " + restricao.restricao
                        tot_contrario += 1
                    elif voto.voto == 'R':
                        tot_favoravel_restricoes += 1
                    elif voto.voto == 'A':
                        tot_abstencao += 1
                    elif voto.voto == 'V':
                        tot_vista += 1
                    votacao.VotoJSONs.append(VotoJSON(voto.vereador.get_full_name(), voto.voto, '', desc_contrario))
                votacao.TotalJSONs.append(TotalJSON(tot_contrario, tot_favoravel, tot_favoravel_restricoes, tot_abstencao, tot_vista))
                asJson = JsonConvert.ToJSON(votacao)
                fromJson = JsonConvert.FromJSON(asJson)
                asJsonFromJson = JsonConvert.ToJSON(fromJson)
                data = jsonref.loads(asJson)
                return JsonResponse(data, safe=False)           
            except Exception as e:
                print('--15')
                print(e)
                asJson = JsonConvert.ToJSON(votacao)
                fromJson = JsonConvert.FromJSON(asJson)
                asJsonFromJson = JsonConvert.ToJSON(fromJson)
                data = jsonref.loads(asJson)
                return JsonResponse(data, safe=False)           
    else:
        return JsonResponse(data, safe=False)           

# -----------------------------------------------------------------------------------
# chamada API para retornar usuarios do sistema
# -----------------------------------------------------------------------------------
def usuarios(request):
    usuarios_json = []
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        e_json = {}
        e_json['id'] = usuario.id
        e_json['first_name'] = usuario.first_name
        e_json['last_name'] = usuario.last_name
        e_json['username'] = usuario.username
        e_json['is_staff'] = usuario.is_staff
        e_json['is_active'] = usuario.is_active
        e_json['is_superuser'] = usuario.is_superuser
        usuarios_json.append(e_json)

    return JsonResponse(usuarios_json, safe=False)
