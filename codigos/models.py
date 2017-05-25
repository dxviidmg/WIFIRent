from django.db import models
from django.utils import timezone

class Codigo(models.Model):
	unidad_duracion_choices = (
		(1, "Hora(s)"),
		(2, "Dia(s)"),
		(3, "Semana(s)"),
		(4, "Mese(s)"),
		(5, "Año(s)"),
	)
	codigo = models.CharField(max_length=20)
	duracion = models.IntegerField()
	unidad_duracion = models.IntegerField(choices=unidad_duracion_choices)
	precio = models.DecimalField(max_digits=6,decimal_places=2)
	creacion = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['unidad_duracion', 'duracion', 'creacion']

	def __str__(self):
		return '{}'.format(self.codigo)