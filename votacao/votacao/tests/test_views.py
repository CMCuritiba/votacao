from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

from autentica.models import User

from votacao.votacao.views import RelatorioVotacaoIndex, RelatorioVotacao

#--------------------------------------------------------------------------------------
# Teste view pesquisa relatório votação
#--------------------------------------------------------------------------------------
class RelatorioVotacaoIndexTest(TestCase):
	
	nome_usuario = 'zaca'
	senha = 'nosferatu'

	def setUp(self):
		self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
		self.user.is_staff = True
		self.user.is_superuser = True
		self.user.save()
		self.factory = RequestFactory()

	def setup_request(self, request):
		request.user = self.user

		middleware = SessionMiddleware()
		middleware.process_request(request)
		request.session.save()

		middleware = MessageMiddleware()
		middleware.process_request(request)
		request.session.save()

	def test_dummy(self):
		self.assertEqual(1,1)		

	def test_view_ok(self):
		request = self.factory.get('/votacao/admin/relatorio/votacao/')
		self.setup_request(request)
		response = RelatorioVotacaoIndex.as_view()(request)
		response.render()
		self.assertEqual(response.status_code, 200)				

#--------------------------------------------------------------------------------------
# Teste view gera relatório votação
#--------------------------------------------------------------------------------------
class RelatorioVotacaoImprimeTest(TestCase):
	
	nome_usuario = 'zaca'
	senha = 'nosferatu'

	def setUp(self):
		self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
		self.user.is_staff = True
		self.user.is_superuser = True
		self.user.save()
		self.factory = RequestFactory()

	def setup_request(self, request):
		request.user = self.user

		middleware = SessionMiddleware()
		middleware.process_request(request)
		request.session.save()

		middleware = MessageMiddleware()
		middleware.process_request(request)
		request.session.save()

	def test_dummy(self):
		self.assertEqual(1,1)		

	def test_view_ok(self):
		request = self.factory.post('/votacao/admin/relatorio/votacao/imprime/', {'pac_id': 683})
		self.setup_request(request)
		response = RelatorioVotacao.as_view()(request)
		self.assertEqual(response.status_code, 200)						