from django.conf.urls import patterns, url
from medicalinfo import views

urlpatterns = patterns('',
	url(r'^$', views.index),
	#url(r'^register/$', views.patient_register, name='patient-register'),
	url(r'^(?P<ref_id>[\w]+)/$', views.medinfo_view,name='med-info-detail'),
	#url(r'^(?P<ref_id>[\w]+)/update/$', views.userprofile_update, name='userprofile-update'),

)