	# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, CharField, DecimalField, DateField, BooleanField
from django.forms.models import inlineformset_factory
from django.forms import formsets, models
from django.forms.models import modelformset_factory
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Button, HTML, ButtonHolder, MultiField, Fieldset
from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, FormActions, AppendedText
from crispy_forms.bootstrap import StrictButton
from django.conf import settings
from decimal import Decimal
from django.utils.safestring import mark_safe

from django.contrib.sessions.backends.db import SessionStore

from votacao.votacao.models import Votacao

#------------------------------------------------------------------------------------------
# classe form utilizada para validar JSON de alteração de status dos locais
#------------------------------------------------------------------------------------------
class JSONVotacaoForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(JSONVotacaoForm, self).__init__(*args, **kwargs)

		self.fields['par_id'] = forms.IntegerField()
		self.fields['pac_id'] = forms.IntegerField()
		self.fields['codigo_projeto'] = forms.CharField()

#------------------------------------------------------------------------------------------
# classe form utilizada para gerar relatório de votação
#------------------------------------------------------------------------------------------
class RelatorioVotacaoIndexForm(forms.Form):

    #def get_grupos(self, request):
        #return GrupoServico.objects.filter(setor__setor_id=request.session['setor_id']).order_by('descricao')


    def __init__(self, *args, **kwargs):
        super(RelatorioVotacaoIndexForm, self).__init__(*args, **kwargs)

        self.fields['data_inicio'] = forms.DateField(label="Data Início")
        self.fields['data_fim'] = forms.DateField(label="Data Fim", required=False)
        self.fields['reuniao'] = forms.ChoiceField(label="Reunião")

        '''

        self.service_helper = ServiceHelper()

        ob_setores = self.service_helper.get_setores_combo('TODOS OS SETORES')
        ob_grupos = self.get_grupos(request)

        self.fields['setor'].choices = [(e.set_id, e.set_nome) for e in ob_setores]
        self.fields['grupo_servico'].choices = [(e.id, e.descricao) for e in ob_grupos]

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Div(
                Div('data_inicio', css_class='col-md-3',),
                Div('data_fim', css_class='col-md-3',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('reuniao', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
        )
        
        '''

#------------------------------------------------------------------------------------------
# classe form utilizada enviar dados seguros para relatório
#------------------------------------------------------------------------------------------
class RelatorioVotacaoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RelatorioVotacaoForm, self).__init__(*args, **kwargs)
        
        self.fields['pac_id'] = forms.IntegerField()