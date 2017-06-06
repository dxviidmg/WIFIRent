from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

class Plan(models.Model):
	nombre = models.CharField(max_length=20)
	unidad_duracion_choices = (
		(1, "Hora(s)"),
		(2, "Dia(s)"),
		(3, "Semana(s)"),
		(4, "Mese(s)"),
		(5, "Año(s)"),
	)	
	duracion = models.IntegerField(verbose_name='Duración')
	unidad_duracion = models.IntegerField(choices=unidad_duracion_choices, verbose_name='Unidad de tiempo')
	precio = models.DecimalField(max_digits=6,decimal_places=2)
	slug = models.SlugField(max_length=40)
	codigos_disponibles = models.IntegerField(default=0)

	class Meta:
		ordering = ['unidad_duracion', 'duracion']

	def __str__(self):
		return '{} {} {}'.format(self.nombre ,self.duracion, self.unidad_duracion)

	def save(self):
		self.slug = slugify(self.nombre)
		super(Plan, self).save()

	def CodigosDisponibles(self):
		plan = Plan.objects.get(pk=self.pk)
		self.codigos_disponibles = Codigo.objects.filter(plan=plan, status=0).count()
		self.save()

class Codigo(models.Model):
	status_choices = (
		(0, "Disponible"),
		(1, "Vendido"),	)
	codigo = models.CharField(max_length=20)
	plan = models.ForeignKey(Plan, null=True)
	creacion = models.DateTimeField(default=timezone.now)
	status = models.IntegerField(choices=status_choices, default=0)

	class Meta:
		ordering = ['creacion']

	def __str__(self):
		return '{}'.format(self.codigo)

	def get_absolute_url(self):
		return reverse('ventas:ViewVentaInicial', kwargs={'codigo': self.codigo})