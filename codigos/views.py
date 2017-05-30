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
	def get(self, request, slug):
		template_name = "codigos/ListViewCodigos.html"
		plan = Plan.objects.get(slug=slug)
		codigos = Codigo.objects.filter(plan=plan, status=0)
		context = {
			'codigos': codigos
		}
		return render(request,template_name, context)