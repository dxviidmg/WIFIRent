from django.db import models
from django.contrib.auth.models import User

def get_full_name(self):
	return '{} {}'.format(self.first_name, self.last_name)

User.add_to_class("__str__", get_full_name)

class PuntoDeVenta(models.Model):	
	Estado_choices = (
		("Hidalgo", "Hidalgo"),
		("Querétaro", "Querétaro"),
	)
	user = models.OneToOneField(User)
	nombre = models.CharField(max_length=50)
	domicilio = models.TextField()
	codigo_postal = models.IntegerField()
	municipio = models.CharField(max_length=50)
	estado = models.CharField(max_length=30, choices=Estado_choices, default="Hidalgo")
	telefono = models.CharField(max_length=20)

	def __str__(self):
		return '{} de {}'.format(self.nombre, self.user)

	class Meta:
		verbose_name_plural = 'Puntos de venta'	