from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .forms import *
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
import datetime

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
		
		NuevoUserNegocioForm = NegocioUserCreateForm()
		NuevoPerfilNegocioForm = NegocioPerfilCreateForm()
		context = {
			'NuevoUserNegocioForm': NuevoUserNegocioForm,
			'NuevoPerfilNegocioForm': NuevoPerfilNegocioForm,			
		}
		return render(request,template_name,context)
	def post(self,request):
		NuevoUserNegocioForm = NegocioUserCreateForm(request.POST)
		NuevoPerfilNegocioForm = NegocioPerfilCreateForm(request.POST)
		dia = datetime.datetime.today().strftime('%d')
		userLast = User.objects.last()

		if NuevoUserNegocioForm.is_valid():
			NuevoUserNegocio = NuevoUserNegocioForm.save(commit=False)
			NuevoUserNegocio.username = "N" + str(dia) + str(userLast.pk+1)
			NuevoUserNegocio.set_password(NuevoUserNegocioForm.cleaned_data['password'])
			NuevoUserNegocio.save()

#		if NuevoPerfilNegocioForm.is_valid():
			NuevoPerfilNegocio = NuevoPerfilNegocioForm.save(commit=False)
			NuevoPerfilNegocio.user = NuevoUserNegocio
			NuevoPerfilNegocio.save()

		return redirect('accounts:ListViewNegocios')

#Eliminar usuario
class DeleteViewNegocio(DeleteView):
	model = User
	success_url = reverse_lazy('accounts:ListViewNegocios')

class ListViewNegocios(View):
	def get(self, request):
		template_name = "accounts/listViewNegocios.html"
		negocios = User.objects.filter(username__startswith="N")
		context = {
			'negocios': negocios
		}
		return render(request,template_name,context)