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

class ListViewUsers(View):
	def get(self, request):
		template_name = "accounts/ListViewUsers.html"
		users = User.objects.exclude(pk=request.user.pk)
		context = {
			'users': users,
		}
		return render(request,template_name, context)

#Creación de un usuario
class CreateViewUser(View):
	@method_decorator(login_required)
	def get(self, request):
		template_name = "accounts/createUser.html"
		
		userForm = UserCreateForm()
		
		context = {
			'userForm': userForm,
		}
		return render(request,template_name,context)
	def post(self,request):
		userForm = UserCreateForm(request.POST)
		if userForm.is_valid():
			nuevoUser = userForm.save(commit=False)
			nuevoUser.set_password(userForm.cleaned_data['password'])
			nuevoUser.save()
		return redirect('accounts:ListViewUsers')

#Eliminar usuario
class DeleteViewUser(DeleteView):
	model = User
	success_url = reverse_lazy('accounts:ListViewUsers')