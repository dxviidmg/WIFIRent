from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from twilio.rest import Client
from django.contrib import messages
from codigos.models import *
from .sms import *

class ViewVenta(View):
#	@method_decorator(login_required)
	def get(self, request, slug):
		plan = Plan.objects.get(slug=slug)
#		print(plan)

		try:
			codigo = Codigo.objects.filter(plan=plan, status="Disponible")[:1].get()
		except Codigo.DoesNotExist:
			codigo = None

#		codigo = Codigo.objects.filter(plan=plan, status="Disponible")[:1].get()
#		print(codigo)
		template_name = "ventas/venta.html"		

		VentaForm = VentaCreateForm()

		context = {
			'plan': plan,
			'codigo': codigo,
			'VentaForm': VentaForm,
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

			r1 = "Código de activación: " + codigo.codigo
			r2 = "\nDuración: " + str(plan.duracion) + " " + plan.unidad_duracion
			r3 = "\nRed: " + plan.punto_venta.nombre_red
			r4 = "\n" + plan.punto_venta.nombre + " agradece su preferencia."
			mensaje = r1 + r2 + r3 + r4
#			print(mensaje)
#			print(telefono, plan.punto_venta)
			status_sms = altiriaSms(telefono ,mensaje, True)
			if status_sms == "OK":
				messages.success(request, "Exito al enviar el código " + codigo.codigo + " enviado al " + telefono)
			else:
				messages.warning(request, "ERROR al enviar el código " + codigo.codigo + " enviado al " + telefono)

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