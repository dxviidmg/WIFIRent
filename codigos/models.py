from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from accounts.models import *

unidad_duracion_choices = (("h", "Hora(s)"), ("d", "Dia(s)"))

class Plan(models.Model):
	punto_venta = models.ForeignKey(PuntoDeVenta)	
	duracion = models.IntegerField(verbose_name='Duración')
	unidad_duracion = models.CharField(max_length=1, choices=unidad_duracion_choices, verbose_name='Unidad de tiempo')
	precio = models.DecimalField(max_digits=6,decimal_places=2)
	codigos_disponibles = models.IntegerField(default=0)
	slug = models.SlugField(max_length=40, blank=True, unique=True)

	class Meta:
		ordering = ['punto_venta', 'unidad_duracion', 'duracion']

	def __str__(self):
		return '{} {} {}'.format(self.duracion, self.unidad_duracion, self.punto_venta)

	class Meta:
		verbose_name_plural = 'Planes'		

	def contar_codigos_disponibles(self):
		plan = Plan.objects.get(pk=self.pk)
		self.codigos_disponibles = Codigo.objects.filter(plan=plan, status="Disponible").count()
		super(Plan, self).save()

	def save(self):
		self.slug= '-'.join((slugify(self.punto_venta.user.username), slugify(self.duracion), slugify(self.unidad_duracion)))
		super(Plan, self).save()

class Codigo(models.Model):
	status_choices = (
		("Disponible", "Disponible"),
		("Vendido", "Vendido")
	)
	codigo = models.CharField(max_length=20)
	plan = models.ForeignKey(Plan, null=True)
	creacion = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=10, choices=status_choices, default="Disponible")

	class Meta:
		ordering = ['creacion']

	def __str__(self):
		return '{}'.format(self.codigo)

	def save(self):
		self.plan.contar_codigos_disponibles()
		super(Codigo, self).save()