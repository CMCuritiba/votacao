from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from unittest.mock import patch, MagicMock, Mock
import json
from django.http import JsonResponse

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
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['status'], 'false')


class JSONTextoConclusaoTest(TestCase):
	def setUp(self):
		super(JSONTextoConclusaoTest, self).setUp()
	
	def test_dummy(self):
		self.assertEqual(1,1)

	@patch('consumer.lib.helper.ServiceHelper.get_textos_conclusao')
	def test_url_ok(self, get_textos_conclusao_mock):
		resp = JsonResponse({}, status=200)
		get_textos_conclusao_mock.return_value = resp
		response = self.client.get('/api/textos_conclusao/005.00087.2018/')
		self.assertEqual(response.status_code, 200)

	@patch('consumer.lib.helper.ServiceHelper.get_textos_conclusao')
	def test_json_data(self, get_textos_conclusao_mock):
		data = {"txt_data": "08/10/2018", "tcp_nome": None, "txt_relator": False, "txt_id": 31851, "txt_finalizado": True, "con_id": 9068, "pro_id": 231127, "tcp_id": None, "vereador": "Julieta Maria Cortes Fialho dos Reis", "ver_id": 19, "pro_codigo": "005.00087.2018", "par_finalizado": False, "par_id": 26433}		
		resp = JsonResponse(data, status=200)
		get_textos_conclusao_mock.return_value = resp
		response = self.client.get('/api/textos_conclusao/005.00087.2018/')
		json = response.json()
		self.assertEqual(json['pro_id'], 231127)
