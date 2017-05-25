from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ViewProfile(View):
	@method_decorator(login_required)
	def get(self, request):
		template_name = "accounts/profile.html"
#		UserForm = UserEditForm(instance=request.user)
		
		context = {
#			'UserForm': UserForm,
#			'PerfilForm': PerfilForm,
		}
		return render(request,template_name, context)
#	def post(self, request):
#		template_name = "accounts/viewProfile.html"
#		perfil = Perfil.objects.get(user=request.user)
#		EdicionUserForm = UserEditForm(instance=request.user, data=request.POST)
#		EdicionPerfilForm = PerfilCreateForm(instance=perfil, data=request.POST, files=request.FILES)

#		if EdicionUserForm.is_valid:
#			EdicionUserForm.save()
#		if EdicionPerfilForm.is_valid:
#			EdicionPerfilForm.save()
#		return redirect('accounts:ViewProfile')