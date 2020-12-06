from django.contrib import admin
from .models import *

#admin.site.register(Codigo)
#admin.site.register(Plan)

class PlanAdmin(admin.ModelAdmin):
	list_display = ['duracion', 'unidad_duracion', 'punto_venta', 'codigos_disponibles']

admin.site.register(Plan, PlanAdmin)

class CodigoAdmin(admin.ModelAdmin):
	list_display = ['codigo', 'plan', 'creacion','status']
	list_filter = ['plan__punto_venta', 'plan', 'status']

admin.site.register(Codigo, CodigoAdmin)

class RecargaAdmin(admin.ModelAdmin):
	date_hierarchy = 'creacion'
	list_display = ['precio', 'cantidad', 'creacion', 'plan', 'autor']
	list_filter = ['plan']

admin.site.register(Recarga, RecargaAdmin)

class PagoAdmin(admin.ModelAdmin):
	date_hierarchy = 'creacion'
	list_display = ['fecha']
	list_filter = ['fecha']

admin.site.register(Pago, PagoAdmin)