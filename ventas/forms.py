from .models import *
from django import forms

class VentaCreateForm(forms.ModelForm):
	class Meta:
		model = Venta
		fields = ('telefono',)

	def clean(self):
		cd = self.cleaned_data
		return cd