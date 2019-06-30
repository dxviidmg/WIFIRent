from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
	#Login
	url(r'^login', login,name="login"),
	url(r'^logout/$', logout, name="logout"),

	#Direccionador
	url(r'^accounts/direccionador/$', views.ViewDireccionador.as_view(), name="ViewDireccionador"),

	#CRUD puntos de venta
	url(r'^puntos_de_venta/delete/(?P<pk>\d+)/$', views.DeleteViewPuntosVenta.as_view(), name="DeleteViewPuntoDeVenta"),
	url(r'^puntos_de_venta/create$', views.CreateViewPuntoDeVenta.as_view(), name="CreateViewPuntoDeVenta"),	
	url(r'^punto_de_venta/edit/(?P<pk>\d+)$', views.UpdateViewPuntoDeVenta.as_view(), name="UpdateViewPuntoDeVenta"),
	url(r'^punto_de_venta/detail/(?P<pk>\d+)$', views.DetailViewPuntoDeVenta.as_view(), name="DetailViewPuntoDeVenta"),
	url(r'^puntos_de_venta/list/$', views.ListViewPuntosDeVenta.as_view(), name="ListViewPuntosDeVenta"),
    ]