from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^plan/(?P<slug>[-\w]+)/codigos/$', views.DetailViewPlan.as_view(), name="DetailViewPlan"),
	url(r'^plan/editar/(?P<slug>[-\w]+)/$', views.UpdateViewPlan.as_view(), name="UpdateViewPlan"),
	url(r'^plan/nuevo$', views.CreateViewPlan.as_view(), name="CreateViewPlan"),
	url(r'^planes/list/$', views.ListViewPlanes.as_view(), name="ListViewPlanes"),
	]