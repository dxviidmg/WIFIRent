from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView

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
		context['codigos'] = Codigo.objects.filter(plan=self.object, status="Disponible")

		context['duracion'] = "hora"
		if self.object.unidad_duracion == "d":
			context['duracion'] = "dia"
		if self.object.duracion > 1:
			context['duracion'] = context['duracion'] + "s"
#		print(context['codigos'])
#		print(self.object)
		return context

class CreateViewCodigo(CreateView):
	model = Codigo
	fields = ['codigo', 'creacion']

	def get_success_url(self):
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		return reverse('codigos:DetailViewPlan',args=(plan.slug,))

	def form_valid(self, form):
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		form.instance.plan = plan
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateViewCodigo, self).get_context_data(**kwargs)
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		context['plan'] = plan
		return context