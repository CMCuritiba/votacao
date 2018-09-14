from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.test import TestCase, Client
from django.urls import reverse
import json

from votacao.votacao.factories import VotacaoFactory

class JSONVotacaoTest(TestCase):
	def setup(self):
		self.factory = APIRequestFactory()

	def test_dummy(self):
		self.assertEqual(1,1)

	def test_url_com_dados(self):
		VotacaoFactory.create()
		response = self.client.post('/api/abre_votacao/667/26393/023.00002.2018/')
		self.assertEqual(response.status_code, 200)		

	def test_url_sem_dados(self):
		votacao = VotacaoFactory.create()
		response = self.client.post('/api/abre_votacao/667/26394/023.00002.2018/')
		self.assertEqual(response.status_code, 200)				


class JSONVerificaAbertoTest(TestCase):
	def setup(self):
		self.factory = APIRequestFactory()

	def test_dummy(self):
		self.assertEqual(1,1)

	def test_url_ok(self):
		VotacaoFactory.create()
		response = self.client.post('/api/verifica_abertos/')
		self.assertEqual(response.status_code, 200)		

	def test_url_aberta(self):
		votacao = VotacaoFactory.create()
		votacao.status = 'A'
		votacao.save()
		response = self.client.post('/api/verifica_abertos/')
		self.assertEqual(response.status_code, 404)						