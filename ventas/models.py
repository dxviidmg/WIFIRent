from django.db import models
from codigos.models import Codigo
from django.utils import timezone
from django.contrib.auth.models import User

class Venta(models.Model):
	codigo = models.OneToOneField(Codigo)
	fecha_hora = models.DateTimeField(default=timezone.now)
	telefono = models.CharField(max_length=10)

	class Meta:
		ordering = ['fecha_hora']

	def __str__(self):
		return '{}'.format(self.codigo)