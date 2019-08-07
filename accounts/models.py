from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

def get_full_name(self):
	return '{} {}'.format(self.first_name, self.last_name)

User.add_to_class("__str__", get_full_name)

class PuntoDeVenta(models.Model):	
	estado_choices = (
		("Hidalgo", "Hidalgo"),
		("Querétaro", "Querétaro"),
	)

	tecnologia_wifi_choices = (
		("Unifi", "Unifi"),
		("Mikrotik", "Mikrotik"),
	)

	user = models.OneToOneField(User)
	nombre = models.CharField(max_length=50, verbose_name='Nombre del punto de venta')
	domicilio = models.TextField()
	codigo_postal = models.IntegerField()
	municipio = models.CharField(max_length=50)
	estado = models.CharField(max_length=30, choices=estado_choices, default="Hidalgo")
	telefono = models.CharField(max_length=20)
	nombre_red = models.CharField(max_length=50, default="test")
	codigos_disponibles = models.IntegerField(default=0)
	saldo_acumulado = models.DecimalField(max_digits=6,decimal_places=2, default=0)	
	porcentaje_comision = models.IntegerField(default=20)
	tecnologia_wifi = models.CharField(max_length=10, default="Unifi", choices=tecnologia_wifi_choices)

	def __str__(self):
		return '{} de {}'.format(self.nombre, self.user)

	class Meta:
		verbose_name_plural = 'Puntos de venta'

	def get_domicilio_completo(self):
		return '{} {} {} {}'.format(self.domicilio, self.codigo_postal, self.municipio, self.estado)


#	def save(self):
#		self.slug= '-'.join((slugify(self.user.username), slugify(self.nombre)))
#		super(PuntoDeVenta, self).save()