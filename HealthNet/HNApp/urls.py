from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from HNApp.views import *

urlpatterns = [
    #Other
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/success/$', views.register_success, name='suc_reg'),
    url(r'^accounts/login/$', views.login_user, name='login'),
    #url(r'^accounts/login/$', views.login_user, kwargs={'success': True}, name='login_with_message'),
    url(r'^login/success/$', views.auth_log, name='auth_log'),
    #Profile
    url(r'^$', views.main_page, name='main_page'),
    url(r'^profile/edit/$', EditProfile.as_view(), name='Edit-profile'),
    #Medical Documents
    url(r'^medical/$', views.medical, name='medical'),
    #Appointments
    url(r'^appointments/$', views.appointments, name='appointments'),
    url(r'^appointments/add/$', AppointmentCreate.as_view(), name='Appointment-add'),
    url(r'^appointments/add/(?P<pk>[0-9]+)/$', AppointmentCreate.as_view(), name='Appointment-add'),
    url(r'^appointments/(?P<pk>[0-9]+)/$', AppointmentUpdate.as_view(), name='Appointment-update'),
    url(r'^appointments/(?P<pk>[0-9]+)/delete/$', AppointmentDelete.as_view(), name='Appointment-delete'),
    #Messages
    url(r'^messages/$', views.messages, name='messages'),
    url(r'^messages/create/$', MessageCreate.as_view(), name='Messages-create'),
    url(r'^messages/reply/(?P<pk>[0-9]+)/$', MessageCreate.as_view(), name='Messages-create'),
    url(r'^messages/(?P<pk>[0-9]+)/$', MessageView.as_view(), name='Messages-view'),
    #Prescriptions
    url(r'^prescriptions/$', views.prescriptions, name='prescriptions'),
    #Patients
    url(r'^patients/$', views.patients, name='patients'),
    url(r'^patients/(?P<pk>[0-9]+)/$', ViewPatientProfile.as_view(), name='View-patient-profile'),
    url(r'^patients/prescription/(?P<pk>[0-9]+)/$', ViewPatientPrescription.as_view(), name='View-patient-prescription'),
    url(r'^patients/appointment/(?P<pk>[0-9]+)/$', ViewPatientAppointment.as_view(), name='View-patient-appointment'),
    url(r'^patients/prescription/write/(?P<pk>[0-9]+)/$', WritePatientPrescription.as_view(), name='Write-patient-prescription'),
    url(r'^patients/upload/(?P<pk>[0-9]+)/$', UploadPatientMedicalDoc.as_view(), name='Upload-patient-medical-doc'),
    #stats
    url(r'^stats/$', views.stats, name='stats'),
    #actitivy logs
    url(r'^activitylog/$', views.ViewActivityLog.as_view(), name='activitylog'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


