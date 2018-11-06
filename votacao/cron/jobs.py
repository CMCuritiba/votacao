# -*- coding: utf-8 -*-
from votacao.votacao.models import Votacao
from datetime import datetime

def fecha_votacoes():
	Votacao.objects.filter(status='A').update(status='V')