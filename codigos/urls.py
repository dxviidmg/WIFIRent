from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^plan/codigos/creados/export/csv/(?P<pk>\d+)/$', views.codigos_recien_creados_csv, name='codigos_recien_creados_csv'),

	url(r'^plan/(?P<slug>[-\w]+)/codigo/crear/$', views.CreateViewCodigo.as_view(), name="CreateViewCodigo"),
	url(r'^plan/(?P<slug>[-\w]+)/recarga/crear/$', views.CreateViewRecarga.as_view(), name="CreateViewRecarga"),
	url(r'^plan/editar/(?P<slug>[-\w]+)/$', views.UpdateViewPlan.as_view(), name="UpdateViewPlan"),
	url(r'^plan/(?P<pk>[-\w]+)/nuevo$', views.CreateViewPlan.as_view(), name="CreateViewPlan"),
	url(r'^recargas/$', views.ListViewRecargas.as_view(), name="ListViewRecargas"),
	]