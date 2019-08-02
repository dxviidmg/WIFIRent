from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
import csv

#Creación de un plan
class CreateViewPlan(CreateView):
	model = Plan
	fields = ['duracion', 'unidad_duracion', 'precio']

	def get_success_url(self):
#		print(self.request.user.puntodeventa, self.object.id,)
		return reverse('accounts:DetailViewPuntoDeVenta',args=(self.object.punto_venta.pk,))

	def form_valid(self, form):
		punto_venta = PuntoDeVenta.objects.get(pk=self.kwargs['pk'])
		form.instance.punto_venta = punto_venta
		return super().form_valid(form)

#Modificación de un plan
class UpdateViewPlan(UpdateView):
	model = Plan
#	success_url = reverse_lazy('accounts:DetailViewPuntoVenta')
	fields = ['duracion', 'unidad_duracion', 'precio']

	def get_success_url(self):
   		return reverse('accounts:DetailViewPuntoDeVenta',args=(self.object.punto_venta.pk,))

class DetailViewPlan(DetailView):
	model = Plan

	def get_context_data(self, **kwargs):
		context = super(DetailViewPlan, self).get_context_data(**kwargs)
		context['recargas'] = Recarga.objects.filter(plan=self.object)

		context['duracion'] = "hora"
		if self.object.unidad_duracion == "d":
			context['duracion'] = "dia"
		if self.object.duracion > 1:
			context['duracion'] = context['duracion'] + "s"
#		print(self.object)
		return context

class CreateViewRecarga(SuccessMessageMixin, CreateView):
	model = Recarga
	fields = ['precio',]

	ultima_recarga = Recarga.objects.latest('pk')
	base = ultima_recarga.pk + 1
	success_message = str(base) + " " +str(ultima_recarga.precio)
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

		ultima_recarga_al_momento = Recarga.objects.latest('pk')
		ultima_recarga = ultima_recarga_al_momento.pk
#		print(base)		
		context['ultima_recarga'] = ultima_recarga
		return context

def codigos_recien_creados_csv(request, pk):
	recarga = Recarga.objects.get(pk=pk)
#	print(recarga)
	plan = Plan.objects.get(recarga=recarga)

	unidad_duracion = "dia"
	if plan.unidad_duracion == "h":
		unidad_duracion = "hora"

	if plan.duracion > 1:
		unidad_duracion = unidad_duracion + "s"

#	print(plan)
#	codigos = Codigo.objects.filter(plan=plan)
#	print(codigos)
	
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="Recarga de $' + str(recarga.precio) + ' del plan ' + str(plan.duracion) + ' ' + str(unidad_duracion) + ' de '+ plan.punto_venta.nombre + ' del '+ recarga.creacion.strftime("%d-%m-%Y %H:%M") +'.csv"'
	writer = csv.writer(response)
#	writer.writerow(['Codigo', 'Zona', 'Plan',])

	codigos = Codigo.objects.filter(plan=plan, status="Disponible").order_by('-id')[:recarga.cantidad].values_list('codigo', 'plan__duracion', 'plan__unidad_duracion')
	for codigo in codigos:
		writer.writerow(['add limit-update=' + str(codigo[1]) + codigo[2] + ' name=' + codigo[0] + ' password=' + codigo[0] + ' profile="' + str(codigo[1]) + codigo[2] + '"'])

	return response	