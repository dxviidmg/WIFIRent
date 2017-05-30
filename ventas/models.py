from django.db import models
from codigos.models import Codigo
from django.utils import timezone
from django.contrib.auth.models import User

class Venta(models.Model):
	codigo = models.OneToOneField(Codigo)
	fecha = models.DateTimeField(default=timezone.now)
	telefono = models.CharField(max_length=10)
	vendedor = models.ForeignKey(User, null=True)

	class Meta:
		ordering = ['fecha']

	def __str__(self):
		return '{}'.format(self.codigo)