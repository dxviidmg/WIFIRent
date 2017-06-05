from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
	url(r'^login', login,name="login"),
	url(r'^logout/$', logout, name="logout"),

	url(r'^accounts/profile/$', views.ViewProfile.as_view(), name="ViewProfile"),

#	url(r'^users/nuevo/$', views.CreateViewUser.as_view(), name="CreateViewUser"),
	url(r'^users/$', views.ListViewUsers.as_view(), name="ListViewUsers"),
    ]