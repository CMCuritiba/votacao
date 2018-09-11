# -*- coding: utf-8 -*-

from factory.django import DjangoModelFactory
from factory import SubFactory
from datetime import datetime

from votacao.votacao.models import Votacao

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
	aberta = False
