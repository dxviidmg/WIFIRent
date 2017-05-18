from django.shortcuts import render
from django.views.generic import View
from twilio.rest import Client

class Prueba(View):
	def get(self, request):
		template_name = "prueba/prueba.html"

		#TWILIO
		account_sid = "ACb647615f13f91027220977cf00e2222b"
		auth_token = "054e4c9c8bc8d103b8fce36ec556da1b"
		my_cell = "+527721403616"
		my_twilio = "+17862313408"

		client = Client(account_sid, auth_token)
		my_message = "Hola mundo"
		message = client.messages.create(to=my_cell, from_=my_twilio, body=my_message)

		return render(request,template_name)