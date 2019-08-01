import requests
from .sms_login import *

def altiriaSms(destinations, message, debug):

	if debug:
#		print('Enter altiriaSms: '+destinations+', message: '+message)

		try:
			#Se crea la lista de parámetros a enviar en la petición POST
			#XX, YY y ZZ se corresponden con los valores de identificación del usuario en el sistema.
			payload = [
			('cmd', 'sendsms'),
			('domainId', domain_id),
			('login', login),
			('passwd', password),
			#No es posible utilizar el remitente en América pero sí en España y Europa
#			('senderId', senderId),
			('msg', message)
			]

			#add destinations
			for destination in destinations.split(","):
				payload.append(('dest', destination))

			#Se fija la codificacion de caracteres de la peticion POST
			contentType = {'Content-Type':'application/x-www-form-urlencoded;charset=utf-8'} 
		
			#Se fija la URL sobre la que enviar la petición POST
			url = 'http://www.altiria.net/api/http'

			#Se envía la petición y se recupera la respuesta
			r = requests.post(url,
			data=payload,
				headers=contentType,
				#Se fija el tiempo máximo de espera para conectar con el servidor (5 segundos)
				#Se fija el tiempo máximo de espera de la respuesta del servidor (60 segundos)
				timeout=(5, 60)) #timeout(timeout_connect, timeout_read)

			if debug:
				if str(r.status_code) != '200': #Error en la respuesta del servidor
					print('ERROR GENERAL: '+ str(r.status_code))
					return 'Error general: '+ str(r.status_code)
				else: #Se procesa la respuesta 
					print('Código de estado HTTP: '+str(r.status_code))
					if (r.text).find("ERROR errNum:"):
						print(r.text[:2])
						if r.text[:2] == "OK":
							return "OK"
						print('Error de Altiria: '+r.text)
						return 'Error de Altiria: '+r.text
					else:
						print('Cuerpo de la respuesta: \n'+r.text)
						return 'Cuerpo de la respuesta: \n'+r.text

			return r.text

		except  requests.ConnectTimeout:
			print("Tiempo de conexión agotado")
			return "Error, Tiempo de conexión agotado"
		
		except  requests.ReadTimeout:
			print("Tiempo de respuesta agotado")
			return "Error, Tiempo de respuesta agotado"

		except Exception as ex:
			if "ascii" in str(ex):
				return "OK", str(ex)
			print("Error interno: " + str(ex))
			return "Error interno: " + str(ex)
