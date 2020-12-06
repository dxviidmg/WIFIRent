from __future__ import unicode_literals
from django.views.generic import View
from django.shortcuts import render
from django.contrib import messages
from .models import *
from codigos.models import *
from .sms import *
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *

class ListViewVentas(View):
	def get(self, request):
		template_name = "ventas/venta_list.html"
		user = User.objects.filter(pk=request.user.pk)
		punto_venta = PuntoDeVenta.objects.filter(user=user)
		planes = Plan.objects.filter(punto_venta=punto_venta)
		codigos = Codigo.objects.filter(plan__in=planes, status="Vendido")
		ventas = Venta.objects.filter(codigo__in=codigos).order_by('-fecha_hora')

		context = {
			'ventas': ventas
		}
		return render(request,template_name, context)

class CreateViewVenta(SuccessMessageMixin, CreateView):
	model = Venta
#	fields = ['telefono']
	form_class = VentaForm
	success_message = "¡Venta realizada!"

	def get_success_url(self):
		print(self.object.codigo.plan.slug)
		return reverse('ventas:CreateViewVenta',args=(self.object.codigo.plan.slug,))

	def form_valid(self, form):
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		tecnologia_wifi = plan.punto_venta.user.antena.tecnologia

		try:
			codigo = Codigo.objects.filter(plan=plan, status="Disponible")[:1].get()
			codigo.status = "Vendido"
			codigo.save()
	
			form.instance.codigo = codigo

			unidad_duracion = "hora"
			if plan.unidad_duracion == "d":
				unidad_duracion = "dia"

			if plan.duracion > 1:
				unidad_duracion = unidad_duracion + "s"

			r1 = "Voucher: "
			if tecnologia_wifi == "Mikrotik":
				r1 = "User and password: "

			r1 = r1 + codigo.codigo
			r2 = "\nTiempo: " + str(codigo.plan.duracion) + " " + unidad_duracion
			r3 = "\nRed: " + plan.punto_venta.user.antena.ssid
			r4 = "\n" + codigo.plan.punto_venta.nombre + " agradece su preferencia."
			renglones = [r1, r2, r3, r4]

			mensaje = " ".join(renglones)
#			print(mensaje)

			form.instance.status_sms = altiriaSms("52" + form.instance.telefono, mensaje, True)
			plan.contar_codigos_disponibles()
		
		except Codigo.DoesNotExist:
			codigo = None
		
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateViewVenta, self).get_context_data(**kwargs)
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		context['plan'] = plan

		unidad_duracion = "hora"
		if plan.unidad_duracion == "d":
			unidad_duracion = "dia"

		if plan.duracion > 1:
			unidad_duracion = unidad_duracion + "s"
		context['unidad_duracion'] = unidad_duracion
		try:
			ultima_venta = Venta.objects.latest('pk')
		except:
			ultima_venta = None
		context['ultima_venta'] = ultima_venta
		return context