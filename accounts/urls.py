from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
	url(r'^login', login,name="login"),
	url(r'^logout/$', logout, name="logout"),

	url(r'^accounts/direccionador/$', views.ViewDireccionador.as_view(), name="ViewDireccionador"),

#	url(r'^negocio/eliminar/(?P<pk>\d+)/$', views.DeleteViewNegocio.as_view(), name="DeleteViewNegocio"),
#	url(r'^negocio/nuevo/$', views.CreateViewNegocio.as_view(), name="CreateViewNegocio"),
	url(r'^puntos_de_venta/$', views.ListViewPuntosDeVenta.as_view(), name="ListViewPuntosVenta"),	

	url(r'^punto_venta/(?P<pk>\d+)$', views.DetailViewPuntoVenta.as_view(), name="DetailViewPuntoVenta"),
    ]