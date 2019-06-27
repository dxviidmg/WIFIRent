from django.contrib import admin
from .models import *

#admin.site.register(Codigo)
#admin.site.register(Plan)

class PlanAdmin(admin.ModelAdmin):
	list_display = ['duracion', 'unidad_duracion', 'punto_venta', 'codigos_disponibles']

admin.site.register(Plan, PlanAdmin)

class CodigoAdmin(admin.ModelAdmin):
	list_display = ['codigo', 'plan', 'creacion','status']
	list_filter = ['plan']
admin.site.register(Codigo, CodigoAdmin)