from django.contrib import admin
from .models import *

class VentaAdmin(admin.ModelAdmin):
	date_hierarchy = 'fecha_hora'
	list_display = ['codigo', 'fecha_hora', 'telefono', 'status_sms']
	list_filter = ['codigo__plan__punto_venta', 'codigo__plan', ]

admin.site.register(Venta, VentaAdmin)