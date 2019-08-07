from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#admin.site.register(PuntoDeVenta)

class PuntoDeVentaAdmin(admin.ModelAdmin):
	list_display = ['nombre', 'user', 'municipio', 'estado', 'tecnologia_wifi']

admin.site.register(PuntoDeVenta, PuntoDeVentaAdmin)

class PuntoDeVentaInline(admin.StackedInline):
	model = PuntoDeVenta
	can_delete = False
	fk_name = 'user'

class CustomUserAdmin(UserAdmin):
	inlines = (PuntoDeVentaInline,)

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)