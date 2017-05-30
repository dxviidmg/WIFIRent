from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^venta/inicial/(?P<codigo>[-\w]+)/$', views.ViewVentaInicial.as_view(), name="ViewVentaInicial"),
		url(r'^ventas/$', views.ListViewVentas.as_view(), name="ListViewVentas"),
    ]