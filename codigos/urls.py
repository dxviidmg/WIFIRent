from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^planes/(?P<slug>[-\w]+)/$', views.ListViewCodigos.as_view(), name="ListViewCodigos"),

	url(r'^planes/borrar/(?P<slug>[-\w]+)/$', views.DeleteViewPlan.as_view(), name="DeleteViewPlan"),
	url(r'^planes/editar/(?P<slug>[-\w]+)/$', views.UpdateViewPlan.as_view(), name="UpdateViewPlan"),
	url(r'^planes/nuevo$', views.CreateViewPlan.as_view(), name="CreateViewPlan"),
	url(r'^planes/$', views.ListViewPlanes.as_view(), name="ListViewPlanes"),
	]