from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from datetime import datetime
from codigos.models import Plan
from random import randint, choice
import string 
from .models import *

now = datetime.now()
#print(now.year)

class ViewDireccionador(View):
	@method_decorator(login_required)
	def get(self, request):
		try:	
			print(request.user.puntodeventa)
			return redirect('accounts:DetailViewPuntoDeVenta', request.user.puntodeventa.pk)
		except:
			return redirect('accounts:ListViewPuntosDeVenta')

class ListViewPuntosDeVenta(ListView):
	model = PuntoDeVenta
#    paginate_by = 100

class PuntoDeVentaInline(InlineFormSetFactory):
	model = PuntoDeVenta
	fields = ['nombre', 'domicilio', 'codigo_postal', 'municipio', 'estado', 'telefono', 'porcentaje_comision', 'nombre_red', 'tecnologia_wifi']

class CreateViewPuntoDeVenta(CreateWithInlinesView):
	model = User
	inlines = [PuntoDeVentaInline]
	fields = ['first_name', 'last_name', 'email']
	template_name = 'accounts/puntodeventa_form.html'
	success_url = reverse_lazy('accounts:ListViewPuntosDeVenta')

	def forms_valid(self, form, inlines):
		last_account = User.objects.last()
		object_pk = last_account.pk + 1
		object_pk = str(object_pk)
		random_number = randint(1,999)
		random_number = str(random_number)
		randon_letter_1 = choice(string.ascii_letters)
		randon_letter_2 = choice(string.ascii_letters)
		form.instance.username = "PV" + randon_letter_1 + randon_letter_2 + object_pk + random_number
		password = "wifirent"
#		print(password)
		form.instance.set_password(password)
		return super(CreateViewPuntoDeVenta, self).forms_valid(form, inlines)

class UpdateViewPuntoDeVenta(UpdateWithInlinesView):
	model = User
	inlines = [PuntoDeVentaInline]
	fields = ['first_name', 'last_name', 'email']
	template_name = 'accounts/puntodeventa_form.html'
	success_url = reverse_lazy('accounts:ListViewPuntosDeVenta')

class DeleteViewPuntosVenta(DeleteView):
	model = User
	success_url = reverse_lazy('accounts:ListViewPuntosDeVenta')

class DetailViewPuntoDeVenta(DetailView):
	model = PuntoDeVenta

	def get_context_data(self, **kwargs):
		context = super(DetailViewPuntoDeVenta, self).get_context_data(**kwargs)
		context['planes'] = Plan.objects.filter(punto_venta=self.object)
#		print(context['codigos'])
#		print(self.object)
		return context