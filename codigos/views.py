from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .forms import *
#from django.views.generic import ListView
from django.views.generic.detail import DetailView

class ListViewCodigosxxx(View):
	@method_decorator(login_required)
	def get(self, request, slug):
		template_name = "codigos/ListViewCodigos.html"
#		plan = Plan.objects.get(slug=slug)
#		codigos = Codigo.objects.filter(plan=plan, status=0)
		codigoForm = CodigoCreateForm()
		context = {
#			'plan': plan,
#			'codigos': codigos,
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
	fields = ['duracion', 'unidad_duracion', 'precio']

	def get_success_url(self):
   		return reverse('accounts:DetailViewPuntoVenta',args=(self.object.id,))

	def form_valid(self, form):
		form.instance.punto_venta = self.request.user.puntodeventa
		return super().form_valid(form)


#Modificación de un plan
class UpdateViewPlan(UpdateView):
	model = Plan
#	success_url = reverse_lazy('accounts:DetailViewPuntoVenta')
	fields = ['duracion', 'unidad_duracion', 'precio']

	def get_success_url(self):
   		return reverse('accounts:DetailViewPuntoVenta',args=(self.object.id,))

#Borrado de un plan
class DeleteViewPlan(DeleteView):
	model = Plan
#	success_url = reverse_lazy('accounts:DetailViewPuntoVenta')

	def get_success_url(self):
   		return reverse('accounts:DetailViewPuntoVenta',args=(self.object.id,))

class DetailViewPlan(DetailView):
	model = Plan

	def get_context_data(self, **kwargs):
		context = super(DetailViewPlan, self).get_context_data(**kwargs)
		context['codigos'] = Codigo.objects.filter(plan=self.object, status="Disponible")
#		print(context['codigos'])
#		print(self.object)
		return context