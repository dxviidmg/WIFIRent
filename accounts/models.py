from django.db import models
from django.contrib.auth.models import User

def get_full_name(self):
	return '{} {}'.format(self.first_name, self.last_name)

User.add_to_class("__str__", get_full_name)

class Perfil(models.Model):	
	Estado_choices = (
		("Hidalgo", "Hidalgo"),
	)
	user = models.OneToOneField(User)
	domicilio = models.CharField(max_length=50, null=True, blank=True)
	codigo_postal = models.IntegerField(null=True, blank=True)
	municipio = models.CharField(max_length=30, null=True, blank=True)
	estado = models.CharField(max_length=30, choices=Estado_choices, default="Hidalgo")
	tipo = models.CharField(max_length=10, null=True, blank=True)


	def __str__(self):
		return '{}'.format(self.user)