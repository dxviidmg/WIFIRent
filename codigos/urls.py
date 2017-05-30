from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^planes/(?P<slug>[-\w]+)/$', views.ListViewCodigos.as_view(), name="ListViewCodigos"),
	url(r'^planes/$', views.ListViewPlanes.as_view(), name="ListViewPlanes"),
	]