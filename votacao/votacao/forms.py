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