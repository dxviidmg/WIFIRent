from django.contrib import admin
from .models import *

class VentaAdmin(admin.ModelAdmin):
	date_hierarchy = 'fecha_hora'
	list_display = ['codigo', 'fecha_hora', 'telefono']

admin.site.register(Venta, VentaAdmin)