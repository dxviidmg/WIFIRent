from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^venta/(?P<slug>[-\w]+)/create/$', views.CreateViewVenta.as_view(), name="CreateViewVenta"),
		url(r'^ventas/$', views.ListViewVentas.as_view(), name="ListViewVentas"),
    ]