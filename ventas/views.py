from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.contrib import messages
from codigos.models import *
from .sms import *
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

class ViewVenta(View):
#	@method_decorator(login_required)
	def get(self, request, slug):
		plan = Plan.objects.get(slug=slug)
#		print(plan)

		try:
			codigo = Codigo.objects.filter(plan=plan, status="Disponible")[:1].get()
		except Codigo.DoesNotExist:
			codigo = None

		unidad_duracion = "hora"
		if plan.unidad_duracion == "d":
			unidad_duracion = "dia"
		if plan.duracion > 1:
			unidad_duracion = unidad_duracion + "s"
#		print(unidad_duracion)

#		codigo = Codigo.objects.filter(plan=plan, status="Disponible")[:1].get()
#		print(codigo)
		template_name = "ventas/venta.html"		

		VentaForm = VentaCreateForm()

		context = {
			'plan': plan,
			'codigo': codigo,
			'VentaForm': VentaForm,
			'unidad_duracion': unidad_duracion
		}
		return render(request,template_name, context)
	def post(self, request, slug):
		template_name = "ventas/venta.html"
		NuevaVentaForm = VentaCreateForm(request.POST)
		plan = Plan.objects.get(slug=slug)
#		print(plan)
		codigo = Codigo.objects.filter(plan=plan, status="Disponible")[:1].get()
#		print(codigo)
		if NuevaVentaForm.is_valid(): 
			NuevaVenta = NuevaVentaForm.save(commit=False)
			NuevaVenta.codigo = codigo
			NuevaVenta.save()

			codigo.status = "Vendido"
			codigo.save()

			telefono = "52" + NuevaVenta.telefono
			
			unidad_duracion = "hora"
			if plan.unidad_duracion == "d":
				unidad_duracion = "dia"
			if plan.duracion > 1:
				unidad_duracion = unidad_duracion + "s"
#			print(unidad_duracion)

			r1 = "Voucher: " + codigo.codigo
			r2 = "\nTiempo: " + str(plan.duracion) + " " + unidad_duracion
			r3 = "\nRed: " + plan.punto_venta.nombre_red
			r4 = "\n" + plan.punto_venta.nombre + " agradece su preferencia."

			renglones = [r1, r2, r3, r4]
			mensaje = " ".join(renglones)
			print(mensaje)
#			print(telefono, plan.punto_venta)
			status_sms = altiriaSms(telefono ,mensaje, True)
			if status_sms == "OK":
				messages.success(request, "Exito al enviar el código " + codigo.codigo + " enviado al " + telefono)
			else:
				messages.warning(request, "ERROR al enviar el código " + codigo.codigo + " enviado al " + telefono + "... " + status_sms)

			plan.contar_codigos_disponibles()

		return redirect("ventas:ViewVenta", plan.slug)

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
	fields = ['telefono']
	success_message = "¡Venta realizada!"

	def get_success_url(self):
		print(self.object.codigo.plan.slug)
		return reverse('ventas:CreateViewVenta',args=(self.object.codigo.plan.slug,))

	def form_valid(self, form):
		plan = Plan.objects.get(slug=self.kwargs['slug'])
		try:
			codigo = Codigo.objects.filter(plan=plan, status="Disponible")[:1].get()
			codigo.status = "Vendido"
			codigo.save()
	
			form.instance.codigo = codigo

			r1 = "Voucher: " + codigo.codigo
			r2 = "\nTiempo: " + str(codigo.plan.duracion) + " " + codigo.plan.unidad_duracion
			r3 = "\nRed: " + codigo.plan.punto_venta.nombre_red
			r4 = "\n" + codigo.plan.punto_venta.nombre + " agradece su preferencia."
			renglones = [r1, r2, r3, r4]
#		renglones = [r1]

			mensaje = " ".join(renglones)
			print(mensaje)

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
		context['ultima_venta'] = Venta.objects.latest('pk')
		return context