from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from unittest.mock import patch, MagicMock, Mock
import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

from votacao.votacao.factories import VotacaoFactory
from votacao.votacao.factories import VereadorFactory
from votacao.votacao.models import Votacao, Voto
from votacao.api.views import vota
from votacao.api.views import reinicia_votacao

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

class JSONVotaVistaTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user('zaquinha', password='zaca')
		self.user.is_staff = True
		self.user.lotado = 171
		self.user.matricula = 2179
		self.user.save()
		self.votacao = Votacao.objects.create(id=1, pac_id = 667, par_id = 26393, codigo_proposicao = '023.00002.2018', status = 'A')
		self.voto = Voto.objects.create(votacao=self.votacao, vereador=self.user, voto='F')
		self.factory = APIRequestFactory()
		super(JSONVotaVistaTest, self).setUp()

	def setup_request(self, request):
		request.user = self.user

		middleware = SessionMiddleware()
		middleware.process_request(request)
		request.session.save()

		middleware = MessageMiddleware()
		middleware.process_request(request)
		request.session.save()
	
	def test_ok(self):
		request = self.factory.post('/api/vota/A/', {'votacao': 1})

		self.setup_request(request)
		response = vota(request, 'V')
		#votacao = VotacaoFactory.create(id=1, pac_id = 667, par_id = 26393, codigo_proposicao = '023.00002.2018', status = 'A')
		self.assertEqual(response.status_code, 200)

class JSONReiniciaVotacaoTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user('zaquinha', password='zaca')
		self.user.is_staff = True
		self.user.lotado = 171
		self.user.matricula = 2179
		self.user.save()
		self.factory = APIRequestFactory()
		super(JSONReiniciaVotacaoTest, self).setUp()

	def setup_request(self, request):
		request.user = self.user

		middleware = SessionMiddleware()
		middleware.process_request(request)
		request.session.save()

		middleware = MessageMiddleware()
		middleware.process_request(request)
		request.session.save()
	
	def test_ok(self):
		self.votacao = Votacao.objects.create(id=1, pac_id = 667, par_id = 26393, codigo_proposicao = '023.00002.2018', status = 'V')
		self.voto = Voto.objects.create(votacao=self.votacao, vereador=self.user, voto='F')

		resp = JsonResponse({'status':'true','message':'Votação reiniciada com sucesso'}, status=200)

		request = self.factory.post('/api/reinicia/', {'pac_id': 667, 'par_id': 26393, 'codigo_proposicao': '023.00002.2018'})

		self.setup_request(request)
		response = reinicia_votacao(request)
		#votacao = VotacaoFactory.create(id=1, pac_id = 667, par_id = 26393, codigo_proposicao = '023.00002.2018', status = 'A')
		self.assertEqual(response.status_code, 200)		
		votacao = Votacao.objects.get(pac_id = 667, par_id = 26393, codigo_proposicao = '023.00002.2018')
		self.assertEqual(votacao.status, 'A')		

	def test_votacao_nao_fechada(self):
		self.votacao = Votacao.objects.create(id=1, pac_id = 667, par_id = 26393, codigo_proposicao = '023.00002.2018', status = 'A')
		self.voto = Voto.objects.create(votacao=self.votacao, vereador=self.user, voto='F')
		
		resp = JsonResponse({'status':'true','message':'Votação reiniciada com sucesso'}, status=200)

		request = self.factory.post('/api/reinicia/', {'pac_id': 667, 'par_id': 26393, 'codigo_proposicao': '023.00002.2018'})

		self.setup_request(request)
		response = reinicia_votacao(request)
		#votacao = VotacaoFactory.create(id=1, pac_id = 667, par_id = 26393, codigo_proposicao = '023.00002.2018', status = 'A')
		self.assertEqual(response.status_code, 404)				

	def test_votacao_nao_encontrada(self):
		self.votacao = Votacao.objects.create(id=1, pac_id = 667, par_id = 26393, codigo_proposicao = '021.00002.2018', status = 'A')
		self.voto = Voto.objects.create(votacao=self.votacao, vereador=self.user, voto='F')
		
		resp = JsonResponse({'status':'true','message':'Votação reiniciada com sucesso'}, status=200)

		request = self.factory.post('/api/reinicia/', {'pac_id': 667, 'par_id': 26393, 'codigo_proposicao': '023.00002.2018'})

		self.setup_request(request)
		response = reinicia_votacao(request)
		#votacao = VotacaoFactory.create(id=1, pac_id = 667, par_id = 26393, codigo_proposicao = '023.00002.2018', status = 'A')
		self.assertEqual(response.status_code, 404)						

class JSONUsuarioTest(TestCase):
	def setup(self):
		self.factory = APIRequestFactory()
		super(JSONUsuarioTest, self).setUp()

	def test_url(self):
		vereador = VereadorFactory.create()	
		response = self.client.get('/api/usuarios/')

		self.assertEqual(response.status_code, 200)
