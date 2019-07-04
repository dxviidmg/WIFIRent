from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^plan/(?P<slug>[-\w]+)/codigo/crear/$', views.CreateViewCodigo.as_view(), name="CreateViewCodigo"),
	url(r'^plan/(?P<slug>[-\w]+)/codigos/$', views.DetailViewPlan.as_view(), name="DetailViewPlan"),
	url(r'^plan/editar/(?P<slug>[-\w]+)/$', views.UpdateViewPlan.as_view(), name="UpdateViewPlan"),
	url(r'^plan/(?P<pk>[-\w]+)/nuevo$', views.CreateViewPlan.as_view(), name="CreateViewPlan"),
	]