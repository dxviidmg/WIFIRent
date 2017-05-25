from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

class Plan(models.Model):
	nombre = models.CharField(max_length=50)
	unidad_duracion_choices = (
		(1, "Hora(s)"),
		(2, "Dia(s)"),
		(3, "Semana(s)"),
		(4, "Mese(s)"),
		(5, "Año(s)"),
	)	
	duracion = models.IntegerField()
	unidad_duracion = models.IntegerField(choices=unidad_duracion_choices)
	precio = models.DecimalField(max_digits=6,decimal_places=2)

	class Meta:
		ordering = ['unidad_duracion', 'duracion']

	def __str__(self):
		return '{} {}'.format(self.duracion, self.unidad_duracion)

	def get_absolute_url(self):
		return reverse('codigos:ListViewCodigos', kwargs={'pk': self.pk})

class Codigo(models.Model):

	status_choices = (
		(0, "Disponible"),
		(1, "vendido"),	)
	codigo = models.CharField(max_length=20)
	plan = models.ForeignKey(Plan, null=True)

	creacion = models.DateTimeField(default=timezone.now)
	status = models.IntegerField(choices=status_choices, default=0)
#	class Meta:
#		ordering = ['unidad_duracion', 'duracion', 'creacion']

	def __str__(self):
		return '{}'.format(self.codigo)