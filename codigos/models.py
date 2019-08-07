from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from accounts.models import *
from decimal import *
from random import randint, choice
import string

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
		self.slug = '-'.join((slugify(self.punto_venta.user.username), slugify(self.duracion), slugify(self.unidad_duracion)))
		super(Plan, self).save()

class Codigo(models.Model):
	status_choices = (
		("Disponible", "Disponible"),
		("Vendido", "Vendido")
	)
	codigo = models.CharField(max_length=11)
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

class Recarga(models.Model):
	plan = models.ForeignKey(Plan)	
	precio = models.DecimalField(max_digits=6,decimal_places=2)	
	cantidad = models.IntegerField(null=True, blank=True)	
	creacion = models.DateTimeField(default=timezone.now)
	autor = models.ForeignKey(User)

	def __str__(self):
		return '{} {} {}'.format(self.precio, self.cantidad, self.creacion)	

#	print(self.plan.precio)

	def save(self):
		porcentaje = self.plan.punto_venta.porcentaje_comision/100 + 1
#		print(porcentaje)
		saldo_total = self.precio* Decimal(porcentaje) + self.plan.punto_venta.saldo_acumulado
		cantidad = saldo_total//self.plan.precio
		saldo_actual = saldo_total - cantidad*self.plan.precio
		self.cantidad = cantidad
#		print(self.plan)

		punto_venta = PuntoDeVenta.objects.get(pk=self.plan.punto_venta.pk)
		punto_venta.saldo_acumulado = saldo_actual
		punto_venta.save()

		if self.plan.punto_venta.tecnologia_wifi == "Mikrotik":
			try:
				ultimo_codigo = Codigo.objects.latest('pk')
				base = ultimo_codigo.pk + 1	
			except:
				base = 1

			codigos = []		

			for n in range(int(cantidad)):
				random_number = str(randint(0,9))
				randon_letter_1 = choice(string.ascii_letters)
				randon_letter_2 = choice(string.ascii_letters)
				randon_letter_3 = choice(string.ascii_letters)
				randon_letter_4 = choice(string.ascii_letters)
				codigo = str(base+n) + random_number + "-" + randon_letter_1 + randon_letter_2 + randon_letter_3 + randon_letter_4
	#			print(codigo)


				codigos.append(Codigo(codigo=codigo, plan=self.plan))
	#		print(codigos)
			Codigo.objects.bulk_create(codigos)
		
		super(Recarga, self).save()	