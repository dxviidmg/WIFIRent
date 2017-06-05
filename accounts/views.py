from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

class ViewProfile(View):
	@method_decorator(login_required)
	def get(self, request):
		template_name = "accounts/profile.html"		
		return render(request,template_name)

class ListViewUsers(View):
	def get(self, request):
		template_name = "accounts/ListViewUsers.html"
		users = User.objects.all()
		context = {
			'users': users,
		}
		return render(request,template_name, context)

