from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

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
	nombre_red = models.CharField(max_length=30, default="test")
	codigos_disponibles = models.IntegerField(default=0)
#	slug = models.SlugField(max_length=40, blank=True, unique=True, null=True)

	def __str__(self):
		return '{} de {}'.format(self.nombre, self.user)

	class Meta:
		verbose_name_plural = 'Puntos de venta'

	def get_domicilio_completo(self):
		return '{} {} {} {} {}'.format(self.domicilio, self.municipio, self.codigo_postal, self.municipio, self.estado)


#	def save(self):
#		self.slug= '-'.join((slugify(self.user.username), slugify(self.nombre)))
#		super(PuntoDeVenta, self).save()