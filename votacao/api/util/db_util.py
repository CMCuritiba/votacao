# -*- coding: utf-8 -*-

from votacao.votacao.models import Votacao

def verifica(status):
	votacoes = Votacao.objects.filter(status=status)
	if votacoes.count() <= 0:
		return True
	else:
		return False
