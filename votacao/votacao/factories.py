# -*- coding: utf-8 -*-

from factory.django import DjangoModelFactory
from factory import SubFactory
from datetime import datetime

from autentica.models import User as Usuario

from votacao.votacao.models import Votacao, Voto, Restricao

#--------------------------------------------------------------------------------------
# Factory Vereador
#--------------------------------------------------------------------------------------
class VereadorFactory(DjangoModelFactory):
	class Meta:
		model = Usuario
	id = 1000
	first_name = 'Vereador Zezinho'
	last_name = 'do Sabará'
	lotado = '111'
	matricula = '22333'
	pessoa = 222
	chefia = False

#--------------------------------------------------------------------------------------
# Factory Votacao
#--------------------------------------------------------------------------------------
class VotacaoFactory(DjangoModelFactory):
	class Meta:
		model = Votacao
	id = 1
	pac_id = 667
	par_id = 26393
	codigo_proposicao = '023.00002.2018'
	status = 'F'

#--------------------------------------------------------------------------------------
# Factory Voto
#--------------------------------------------------------------------------------------
class VotoFactory(DjangoModelFactory):
	class Meta:
		model = Voto
	id = 1
	votacao = SubFactory(VotacaoFactory)
	vereador = SubFactory(VereadorFactory)
	voto = 'F'

#--------------------------------------------------------------------------------------
# Factory Restricao
#--------------------------------------------------------------------------------------
class RestricaoFactory(DjangoModelFactory):
	class Meta:
		model = Restricao
	id = 1
	voto = SubFactory(VotoFactory)
	restricao = 'Há controvérsias'
