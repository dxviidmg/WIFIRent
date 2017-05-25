from django.db import models
from codigos.models import Codigo
from django.utils import timezone

class Venta(models.Model):
	codigo = models.OneToOneField(Codigo)
	creacion = models.DateTimeField(default=timezone.now)
	telefono = models.CharField(max_length=10)

	class Meta:
		ordering = ['creacion']

	def __str__(self):
		return '{}'.format(self.codigo)