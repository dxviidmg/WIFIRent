from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .forms import *

class ListViewPlanes(View):
	@method_decorator(login_required)
	def get(self, request):
		template_name = "codigos/ListViewPlanes.html"		
#		negocio = get_object_or_404(User, pk=pk)
#		planes = Plan.objects.filter(negocio=negocio)
		context = {
#			'planes': planes
		}
		return render(request,template_name, context)

class ListViewCodigos(View):
	@method_decorator(login_required)
	def get(self, request, slug):
		template_name = "codigos/ListViewCodigos.html"
		plan = Plan.objects.get(slug=slug)
		codigos = Codigo.objects.filter(plan=plan, status=0)
		codigoForm = CodigoCreateForm()
		context = {
			'plan': plan,
			'codigos': codigos,
			'codigoForm': codigoForm
		}
		return render(request,template_name, context)

	def post(self,request, slug):
		template_name = "codigos/ListViewCodigos.html"
		plan = Plan.objects.get(slug=slug)


		codigoForm = CodigoCreateForm(request.POST)
		if codigoForm.is_valid():
			nuevoCodigo = codigoForm.save(commit=False)
			nuevoCodigo.plan = plan
			nuevoCodigo.save()
		return redirect("codigos:ListViewCodigos", slug=plan.slug) 		

#Creación de un plan
class CreateViewPlan(CreateView):
	model = Plan
	success_url = reverse_lazy('codigos:ListViewPlanes')
	fields = ['nombre', 'duracion', 'unidad_duracion', 'precio']

#Modificación de un plan
class UpdateViewPlan(UpdateView):
	model = Plan
	success_url = reverse_lazy('codigos:ListViewPlanes')
	fields = ['nombre', 'duracion', 'unidad_duracion', 'precio']

#Borrado de un plan
class DeleteViewPlan(DeleteView):
	model = Plan
	success_url = reverse_lazy('codigos:ListViewPlanes')