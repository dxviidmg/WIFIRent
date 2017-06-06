from django import forms
from .models import *

class CodigoCreateForm(forms.ModelForm):
	class Meta:
		model = Codigo
		fields = ( 'codigo',)

		labels = {
			"codigo": "Código"
		}