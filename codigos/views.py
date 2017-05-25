from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *

class ListViewPlanes(View):
	@method_decorator(login_required)
	def get(self, request):
		template_name = "codigos/ListViewPlanes.html"		
		planes = Plan.objects.all()
		context = {
			'planes': planes
		}
		return render(request,template_name, context)

class ListViewCodigos(View):
	@method_decorator(login_required)
	def get(self, request, pk):
		template_name = "codigos/ListViewCodigos.html"
		plan = Plan.objects.get(pk=pk)
		codigos = Codigo.objects.filter(plan=plan)
		context = {
			'codigos': codigos
		}
		return render(request,template_name, context)