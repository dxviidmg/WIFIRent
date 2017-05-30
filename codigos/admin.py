from django.contrib import admin
from .models import *

admin.site.register(Codigo)
#admin.site.register(Plan)

class PlanAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}

admin.site.register(Plan, PlanAdmin)