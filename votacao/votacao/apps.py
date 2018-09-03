# -*- coding: utf-8 -*-

from django.apps import AppConfig


class VotacaoConfig(AppConfig):
    name = 'votacao.votacao'
    verbose_name = "VOTACAO"

    def ready(self):
        pass
