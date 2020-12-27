from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
import csv
from django.views.generic import View
from django.shortcuts import render

#Creación de un plan
class CreateViewPlan(CreateView):
	model = Plan
	fields = ['duracion', 'unidad_duracion', 'precio', 'velocidad_descarga', 'unidad_velocidad_descarga', 'velocidad_subida', 'unidad_velocidad_subida', 'observaciones']

	def get_success_url(self):
		return reverse('accounts:DetailViewPuntoDeVenta',args=(self.object.punto_venta.pk,))

	def form_valid(self, form):
		punto_venta = PuntoDeVenta.objects.get(pk=self.kwargs['pk'])
		form.instance.punto_venta = punto_venta
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateViewPlan, self).get_context_data(**kwargs)
		punto_venta = PuntoDeVenta.objects.get(pk=self.kwargs['pk'])
		context['punto_venta'] = punto_venta
		return context
		
#Modificación de un plan
class UpdateViewPlan(UpdateView):
	model = Plan
#	success_url = reverse_lazy('accounts:DetailViewPuntoVenta')
	fields = ['duracion', 'unidad_duracion', 'precio', 'velocidad_descarga', 'unidad_velocidad_descarga', 'velocidad_subida', 'unidad_velocidad_subida', 'observaciones']

	def get_success_url(self):
   		return reverse('accounts:DetailViewPuntoDeVenta',args=(self.object.punto_venta.pk,))

class ListViewRecargas(View):
	def get(self, request):
		template_name = "codigos/recarga_list.html"
		user = User.objects.filter(pk=request.user.pk)
		punto_venta = PuntoDeVenta.objects.filter(user=user)
		planes = Plan.objects.filter(punto_venta=punto_venta)
		recargas = Recarga.objects.filter(plan__in=planes).order_by('-id')

		context = {
			'recargas': recargas
		}
		return render(request,template_name, context)

class CreateViewRecarga(SuccessMessageMixin, CreateView):
	model = Recarga
	fields = ['precio',]

#	ultima_recarga = Recarga.objects.latest('pk')
#	base = ultima_recarga.pk + 1
	success_message = "¡Recarga exitosa!"
#	print(success_message)

	def get_success_url(self):
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		return reverse('codigos:CreateViewRecarga',args=(plan.slug,))

	def form_valid(self, form):
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		form.instance.plan = plan
		form.instance.autor = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateViewRecarga, self).get_context_data(**kwargs)
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		context['plan'] = plan

		unidad_duracion = "hora"
		if plan.unidad_duracion == "d":
			unidad_duracion = "dia"

		if plan.duracion > 1:
			unidad_duracion = unidad_duracion + "s"
		context['unidad_duracion'] = unidad_duracion

		try:
			context['ultima_recarga'] = Recarga.objects.latest('pk')
		except:
			context['ultima_recarga'] = None

		return context

def codigos_recien_creados_csv(request, pk):
	recarga = Recarga.objects.get(pk=pk)
#	print(recarga)
	plan = Plan.objects.get(recarga=recarga)

	unidad_duracion = "dia"
	limit_update = str(plan.duracion) + plan.unidad_duracion
	
	if plan.unidad_duracion == "h":
		unidad_duracion = "hora"
		limit_update = str(plan.duracion) + ":00:00"
		if len(limit_update) == 7:
			limit_update = "0" + limit_update
#	print(limit_update)

	if plan.duracion > 1:
		unidad_duracion = unidad_duracion + "s"

#	print(plan)
#	codigos = Codigo.objects.filter(plan=plan)
#	print(codigos)
	
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="Recarga de $' + str(recarga.precio) + ' del plan ' + str(plan.duracion) + ' ' + str(unidad_duracion) + ' de '+ plan.punto_venta.nombre + ' del '+ recarga.creacion.strftime("%d-%m-%Y %H:%M") +'.csv"'
	writer = csv.writer(response)
#	writer.writerow(['Codigo', 'Zona', 'Plan',])

	codigos = Codigo.objects.filter(plan=plan, status="Disponible").order_by('-id')[:recarga.cantidad].values_list('codigo')
	for codigo in codigos:
		writer.writerow(['/ip hotspot user add limit-uptime=' + limit_update + ' name=' + codigo[0] + ' password=' + codigo[0] + ' profile="' + str(plan.duracion) + plan.unidad_duracion + '" server=hotspot1'])

	return response

class CreateViewCodigo(SuccessMessageMixin, CreateView):
	model = Codigo
	fields = ['codigo',]

#	ultimo_codigo = Codigo.objects.latest('pk')
#	base = ultima_c.pk + 1
	success_message = "¡Código exitoso!"
#	print(success_message)

	def get_success_url(self):
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		return reverse('codigos:CreateViewCodigo',args=(plan.slug,))

	def form_valid(self, form):
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		form.instance.plan = plan
#		form.instance.autor = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateViewCodigo, self).get_context_data(**kwargs)
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		context['plan'] = plan

		unidad_duracion = "hora"
		if plan.unidad_duracion == "d":
			unidad_duracion = "dia"

		if plan.duracion > 1:
			unidad_duracion = unidad_duracion + "s"
		context['unidad_duracion'] = unidad_duracion
#
		try:
			ultimo_codigo = Codigo.objects.latest('pk')
			context['ultimo_codigo'] = ultimo_codigo
		except:
			ultimo_codigo = None
		return context	


class TutorialComisionView(View):
	def get(self, request):
		template = "codigos/tutorial_comision.html"
		return render(request, template)