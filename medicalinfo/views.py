from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import UserProfile, Employee, Doctor, Nurse
from medicalinfo.models import MedicalInformation
from django.contrib import messages
import datetime


from accounts.forms import (UserCreationForm, UserProfileForm, 
	NewPatientForm, AuthenticationForm, EmployeeCreationForm

)

from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)



def check_user(request_ref_id, ref_id):
	return request_ref_id == ref_id

@login_required
@permission_required('medicalinfo.change_medicalinformation', raise_exception=True)
def medinfo_view(request, ref_id):
	template_name= 'medicalinfo/medinfo_view_form.html'
	context = {}
	#messages.warning(request, "Opps, are you in the right place?")
	return render(request, template_name, context)


@login_required(login_url='/account/login')
def userprofile_update(request, ref_id):
	'''check if request user is the same logged in user'''
	if check_user(request.user.userprofile.ref_id,ref_id):
		template_name = 'accounts/account_profile_udpate_form.html'
		

		context = {}
		profile = UserProfile.objects.get(ref_id=ref_id)
		form = UserProfileForm(request.POST or None, instance=profile)

		if request.method == 'POST':
			if form.is_valid():
				form.save()
				messages.success(request, 'You have successfully updated your profile information')
				return redirect('/account/message')

		context['form'] = form

		return render(request, template_name, context)
	else:
		template_name= 'accounts/account_message.html'
		patients = Patient.objects.all()
		context = {'patients' : patients}
		messages.warning(request, "Opps, are you in the right place?")
		return render(request, template_name, context)



