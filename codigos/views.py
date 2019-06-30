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
   		return reverse('accounts:DetailViewPuntoDeVenta',args=(self.request.user.puntodeventa.pk,))

	def form_valid(self, form):
		form.instance.punto_venta = self.request.user.puntodeventa
		return super().form_valid(form)

#Modificación de un plan
class UpdateViewPlan(UpdateView):
	model = Plan
#	success_url = reverse_lazy('accounts:DetailViewPuntoVenta')
	fields = ['duracion', 'unidad_duracion', 'precio']

	def get_success_url(self):
   		return reverse('accounts:DetailViewPuntoDeVenta',args=(self.request.user.puntodeventa.pk,))

class DetailViewPlan(DetailView):
	model = Plan

	def get_context_data(self, **kwargs):
		context = super(DetailViewPlan, self).get_context_data(**kwargs)
		context['codigos'] = Codigo.objects.filter(plan=self.object, status="Disponible")
#		print(context['codigos'])
#		print(self.object)
		return context