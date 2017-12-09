from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
	url(r'^login', login,name="login"),
	url(r'^logout/$', logout, name="logout"),

	url(r'^accounts/profile/$', views.ViewProfile.as_view(), name="ViewProfile"),

	url(r'^negocio/eliminar/(?P<pk>\d+)/$', views.DeleteViewNegocio.as_view(), name="DeleteViewNegocio"),
	url(r'^negocio/nuevo/$', views.CreateViewNegocio.as_view(), name="CreateViewNegocio"),
	url(r'^negocios/$', views.ListViewNegocios.as_view(), name="ListViewNegocios"),	
    ]