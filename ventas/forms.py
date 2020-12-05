from django import forms
from .models import Venta

class VentaForm(forms.ModelForm):
	telefono2 = forms.CharField(label='Repite tu teléfono',widget=forms.TextInput)

	class Meta:
		model = Venta
		fields = ('telefono',)

	def clean_telefono2(self):
		cd = self.cleaned_data
		if cd['telefono'] != cd['telefono2']:
			raise forms.ValidationError('El teléfono no coincide')
		return cd['telefono']