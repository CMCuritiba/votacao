# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from datetime import datetime

from autentica.models import User as Usuario

#---------------------------------------------------------------------------------------------
# Model Votacao
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class Votacao(models.Model):
	class Meta:
		verbose_name_plural = 'Votações'

	pac_id = models.IntegerField()
	par_id = models.IntegerField(unique=True)
	codigo_proposicao = models.CharField(max_length=20)
	status = models.CharField(max_length=1, default='F') # (A)berta, (F)echada, (V)otada

	def __unicode__(self):
		return self.codigo_proposicao

	def __str__(self):
		return self.codigo_proposicao

#---------------------------------------------------------------------------------------------
# Model Voto
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class Voto(models.Model):
	class Meta:
		verbose_name_plural = 'Votos'

	FAVORAVEL = 'F'
	FAVORAVEL_RESTRICOES = 'R'
	CONTRARIO = 'C'
	ABSTENCAO = 'A'
	VISTA = 'V'

	VOTO_CHOICES = (
		(FAVORAVEL, 'FAVORÁVEL'),
		(FAVORAVEL_RESTRICOES, 'FAVORÁVEL COM RESTRIÇÕES'),
		(CONTRARIO, 'CONTRÁRIO'),
		(VISTA, 'VISTA'),
		(ABSTENCAO, 'ABSTENÇÃO'),
	)

	votacao = models.ForeignKey(Votacao, on_delete=models.PROTECT)
	vereador = models.ForeignKey(Usuario, on_delete=models.PROTECT)
	voto = models.CharField(max_length=1, choices=VOTO_CHOICES)

	def __unicode__(self):
		return self.votacao.codigo_proposicao

	def __str__(self):
		return self.votacao.codigo_proposicao
