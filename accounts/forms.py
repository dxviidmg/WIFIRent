from django import forms
from .models import *

class UserCreateForm(forms.ModelForm):
	password = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repite tu password',widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username','first_name', 'last_name', 'email',)
	
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Los passwords no coicinden')
		return cd['password2']

	def clean_username(self):
	    username = self.cleaned_data['username']
	    try:
	        user = User.objects.exclude(pk=self.instance.pk).get(username=username)
	    except User.DoesNotExist:
	        return username
	    raise forms.ValidationError(u'El usuario "%s" ya esta en uso.' % username)