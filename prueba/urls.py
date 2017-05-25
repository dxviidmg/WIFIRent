from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^prueba/$',views.Prueba.as_view(), name='prueba'),
]