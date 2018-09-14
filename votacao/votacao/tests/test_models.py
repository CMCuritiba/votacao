# -*- coding: utf-8 -*-

from django.test import TestCase, Client, RequestFactory
from django.db import IntegrityError, DataError
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime

from votacao.votacao.factories import VotoFactory, VotacaoFactory, RestricaoFactory

#--------------------------------------------------------------------------------------
# Testes model Voto
#--------------------------------------------------------------------------------------
class VotoModelTest(TestCase):
	
	nome_usuario = 'zaca'
	senha = 'nosferatu'

	def setUp(self):
		self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
		self.user.is_staff = True
		self.user.save()
		self.factory = RequestFactory()

	def test_dummy(self):
		self.assertEqual(1,1)

	def test_local_status_ok(self):
		voto = VotoFactory.create()
		self.assertEqual(voto.id, 1)


	def test_insere_voto_nulo(self):
		with self.assertRaises(IntegrityError):
			voto = VotoFactory.create(voto=None)

#--------------------------------------------------------------------------------------
# Testes model Votacao
#--------------------------------------------------------------------------------------
class VotacaoModelTest(TestCase):
	
	nome_usuario = 'zaca'
	senha = 'nosferatu'

	def setUp(self):
		self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
		self.user.is_staff = True
		self.user.save()
		self.factory = RequestFactory()

	def test_dummy(self):
		self.assertEqual(1,1)

	def test_votacao_status_ok(self):
		votacao = VotacaoFactory.create()
		self.assertEqual(votacao.id, 1)

#--------------------------------------------------------------------------------------
# Testes model Restricao
#--------------------------------------------------------------------------------------
class RestricaoModelTest(TestCase):
	
	nome_usuario = 'zaca'
	senha = 'nosferatu'

	def setUp(self):
		self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
		self.user.is_staff = True
		self.user.save()
		self.factory = RequestFactory()

	def test_dummy(self):
		self.assertEqual(1,1)

	def test_restricao_ok(self):
		restricao = RestricaoFactory.create()
		self.assertEqual(restricao.id, 1)		

