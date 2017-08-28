from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from twilio.rest import Client
from django.contrib import messages

class ViewVentaInicial(View):
#	@method_decorator(login_required)
	def get(self, request, codigo):
		template_name = "ventas/ViewVentaInicial.html"		

		VentaForm = VentaCreateForm()

		context = {
			'VentaForm': VentaForm,
		}
		return render(request,template_name, context)
	def post(self, request, codigo):
		template_name = "ventas/ViewVentaInicial.html"
		NuevaVentaForm = VentaCreateForm(request.POST)
		codigo = Codigo.objects.get(codigo=codigo)
		vendedor = User.objects.get(pk=request.user.pk)

		if NuevaVentaForm.is_valid(): 
			NuevaVenta = NuevaVentaForm.save(commit=False)
			NuevaVenta.codigo = codigo
			NuevaVenta.vendedor = vendedor
			NuevaVenta.save()

			codigo.status = 1
			codigo.save()

			#TWILIO
			account_sid = "AC6632ff16a27f7eaa259469bd474cdf05"
			auth_token = "f36b4971dc478cc2954732685c6d1a68"
			my_cell = "+52" + NuevaVenta.telefono
			my_twilio = "+17862313408"

			client = Client(account_sid, auth_token)
			my_message = NuevaVenta.codigo
			message = client.messages.create(to=my_cell, from_=my_twilio, body=my_message)

			messages.success(request, "¡¡¡Mensaje enviado!!!")
		return redirect("ventas:ViewVentaInicial", codigo)

class ListViewVentas(View):
	def get(self, request):
		template_name = "ventas/ListViewVentas.html"		

		ventas = Venta.objects.all().order_by('-fecha')[:30]

		context = {
			'ventas': ventas
		}
		return render(request,template_name, context)