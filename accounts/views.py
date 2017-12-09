from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .forms import *
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy

class ViewProfile(View):
	@method_decorator(login_required)
	def get(self, request):
		template_name = "accounts/profile.html"		
		return render(request,template_name)

class ListViewNegocios(View):
	def get(self, request):
		template_name = "accounts/ListViewNegocios.html"
		Negocios = User.objects.exclude(pk=request.Negocio.pk)
		context = {
			'Negocios': Negocios,
		}
		return render(request,template_name, context)

#Creación de un usuario
class CreateViewNegocio(View):
	@method_decorator(login_required)
	def get(self, request):
		template_name = "accounts/createNegocio.html"
		
		NegocioForm = NegocioCreateForm()
		
		context = {
			'NegocioForm': NegocioForm,
		}
		return render(request,template_name,context)
	def post(self,request):
		NegocioForm = NegocioCreateForm(request.POST)
		if NegocioForm.is_valid():
			nuevoNegocio = NegocioForm.save(commit=False)
			nuevoNegocio.set_password(NegocioForm.cleaned_data['password'])
			nuevoNegocio.save()
		return redirect('accounts:ListViewNegocios')

#Eliminar usuario
class DeleteViewNegocio(DeleteView):
	model = User
	success_url = reverse_lazy('accounts:ListViewNegocios')

class ListViewNegocios(View):
	def get(self, request):
		template_name = "accounts/listViewNegocios.html"
		negocios = User.objects.filter(perfil__tipo="Negocio")
		context = {
			'negocios': negocios
		}
		return render(request,template_name,context)