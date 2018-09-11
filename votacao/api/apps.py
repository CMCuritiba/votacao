# -*- coding: utf-8 -*-

from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'votacao.api'
    verbose_name = "API"

    def ready(self):
        pass
