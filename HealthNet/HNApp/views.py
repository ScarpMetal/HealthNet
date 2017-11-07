from django.shortcuts import render
from HNApp.models import *
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .forms import *
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#from dal import autocomplete
from django.utils.timezone import localtime, now
from django.db.models import Q
from django.views.generic import View

########## here begins the medical views ##########
@login_required()
def medical(request):
    user = request.user
    ActivityLog.objects.create(person=user.person, time=now(), act="View Medical Docs")
    if Patient.objects.filter(user=user).exists():
        patient = user.person
        medical_docs = MedicalDocument.objects.filter(patient=patient)
        return render(request, 'HNApp/patient/medical.html', {'medical': medical_docs})

    medical_docs= ('',)
    return render(request, 'HNApp/patient/medical.html', {'medical': medical_docs})

########## here begins the appointments views ##########
@login_required()
def appointments(request):
    user = request.user
    ActivityLog.objects.create(person=user.person, time=now(), act="View Appointment")
    if Patient.objects.filter(user=user).exists():
        patient = user.person
        appts = Appointment.objects.filter(patient=patient)
        return render(request, 'HNApp/patient/appointments.html', {'appointments': appts})

    if Doctor.objects.filter(user=user).exists():
        doctor = user.person
        appts = Appointment.objects.filter(doctor=doctor)
        return render(request, 'HNApp/doctor/appointments_doctor.html', {'appointments': appts})

    appts= ('',)
    return render(request, 'HNApp/patient/appointments.html', {'appointments': appts})

class AppointmentDelete(View):
    #model = Appointment
    #success_url = reverse_lazy('appointments')
    def get(self, request, *args, **kwargs):
        user = request.user

        if Patient.objects.filter(user=user).exists():
            return render(request, 'HNApp/patient/appointment_confirm_delete.html')
        if Doctor.objects.filter(user=user).exists():
            return render(request, 'HNApp/doctor/appointment_confirm_delete_doctor.html')

    def post(self, request, *args, **kwargs):
        appt = Appointment.objects.get(id=kwargs['pk'])
        user = request.user
        ActivityLog.objects.create(person=user.person, time=now(), act="Delete Appointment")
        appt.delete()
        return HttpResponseRedirect('/appointments/')

class AppointmentUpdate(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        appt = Appointment.objects.get(id=kwargs['pk'])
        doctor = [appt.doctor]
        patient = [appt.patient]
        time = appt.time
        date = appt.date
        desc = appt.description
        if Patient.objects.filter(user=user).exists():
            form = CreateAppointmentFormPatient(initial={'doctor': doctor, 'patient': patient, 'time': time,
                                                        'date': date, 'desc': desc})
            return render(request, 'HNApp/patient/appointment_create.html', {'form': form,
                                                                             'header': "Update Appointment",
                                                                             'button': "Update"})
        if Doctor.objects.filter(user=user).exists():
            form = CreateAppointmentFormDoctor(initial={'doctor': doctor, 'patient': patient, 'time': time,
                                                        'date': date, 'description': desc})
            return render(request, 'HNApp/doctor/appointment_create_doctor.html', {'form': form,
                                                                                   'header': "Update Appointment",
                                                                                   'button': "Update"})

    def post(self, request, *args, **kwargs):
        user = request.user
        if Patient.objects.filter(user=user).exists():
            form = CreateAppointmentFormPatient(request.POST)

        if Doctor.objects.filter(user=user).exists():
            form = CreateAppointmentFormDoctor(request.POST)

        if form.is_valid():
            user = request.user
            appt = Appointment.objects.get(id=next(iter(kwargs.values())))
            #gets data from the form
            if Patient.objects.filter(user=user).exists():
                patient = Patient.objects.get(user=user)
                doctor = form.cleaned_data['doctor'][0]
            if Doctor.objects.filter(user=user).exists():
                patient = form.cleaned_data['patient'][0]
                doctor = Doctor.objects.get(user=user)
            time = form.cleaned_data['time']
            date = form.cleaned_data['date']
            desc = form.cleaned_data['description']
            ActivityLog.objects.create(person=user.person, time=now(), act="Appointment update")
            #updates information in the appointment
            appt.patient = patient
            appt.doctor = doctor
            appt.time = time
            appt.date = date
            appt.description = desc
            appt.save()
            return HttpResponseRedirect('/appointments/')

class AppointmentCreate(View):
    init = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        if len(kwargs) != 0:
            patient = Patient.objects.get(id=kwargs['pk'])
            patient = [patient]
            self.init = {'patient': patient}
        user = request.user
        if Patient.objects.filter(user=user).exists():
            form = CreateAppointmentFormPatient(initial=self.init)
            return render(request, 'HNApp/patient/appointment_create.html', {'form': form,
                                                                             'header': "Create Appointment",
                                                                             'button': "Create"})

        if Doctor.objects.filter(user=user).exists():
            form = CreateAppointmentFormDoctor(initial=self.init)
            return render(request, 'HNApp/doctor/appointment_create_doctor.html', {'form': form,
                                                                                   'header': "Create Appointment",
                                                                                   'button': "Create"})

    def post(self, request, *args, **kwargs):
        user = request.user
        if Patient.objects.filter(user=user):
            form = CreateAppointmentFormPatient(request.POST)

        if Doctor.objects.filter(user=user):
            form = CreateAppointmentFormDoctor(request.POST)

        if form.is_valid():
            if Patient.objects.filter(user=user).exists():
                patient = Patient.objects.get(user=user)
                doctor = form.cleaned_data['doctor'][0]

            if Doctor.objects.filter(user=user).exists():
                patient = form.cleaned_data['patient'][0]
                doctor = Doctor.objects.get(user=user)

            time = form.cleaned_data['time']
            date = form.cleaned_data['date']
            # bounce them back for duplicate appointments
            if Appointment.objects.filter(time=time, date=date, doctor=doctor).exists():
                return HttpResponseRedirect('/appointments/add/')
            description = form.cleaned_data['description']
            Appointment.objects.create(patient=patient, doctor=doctor, time=time, date=date, description=description)
            ActivityLog.objects.create(person=user.person, time=now(), act="Appointment Created")
            doctor.patients.add(patient)
            doctor.save()
            return HttpResponseRedirect('/appointments/')
        return HttpResponseRedirect('/appointments/add/')


########## here begins the prescriptions views ##########
@login_required()
def prescriptions(request):
    user = request.user
    if Patient.objects.filter(user=user).exists():
        patient = user.person
        prescriptions = Prescription.objects.filter(patient=patient)
        ActivityLog.objects.create(person=user.person, time=now(), act="View Prescriptions")
        return render(request, 'HNApp/patient/prescriptions.html', {'prescriptions': prescriptions})

    prescriptions= ('',)
    return render(request, 'HNApp/patient/prescriptions.html')

########## here begins the messages views ##########
@login_required()
def messages(request):
    user = request.user
    if Person.objects.filter(user=user).exists():
        person = user.person
        msgs = Message.objects.filter(Q(sender=person)|Q(receiver=person)).order_by('-date', '-time')
        ActivityLog.objects.create(person=user.person, time=now(), act="View Messages")
        if Patient.objects.filter(user=user).exists():
            return render(request, 'HNApp/patient/messages.html', {'messages': msgs,
                                                                   'today': localtime(now()).date()})
        if Doctor.objects.filter(user=user).exists():
            return render(request, 'HNApp/doctor/messages_doctor.html', {'messages': msgs,
                                                                         'today': localtime(now()).date()})

    #messages= ('',)
    #return render(request, 'HNApp/patient/messages.html')

class MessageCreate(View):
    form_class = MessageForm
    init = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        if len(kwargs) != 0:
            message = Message.objects.get(id=kwargs['pk'])
            label = "RE:" + message.label
            person = Person.objects.get(id=message.sender.id)
            person = [person]
            self.init = {'receiver': person, 'label': label}
        user = request.user
        form = self.form_class(initial=self.init)
        if Patient.objects.filter(user=user).exists():
            return render(request, 'HNApp/patient/messages_create.html', {'form': form})
        if Doctor.objects.filter(user=user).exists():
            return render(request, 'HNApp/doctor/messages_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            sender = Person.objects.get(user=user)
            r = form.cleaned_data['receiver']
            receiver = r[0]
            label = form.cleaned_data['label']
            msg = form.cleaned_data['message']
            Message.objects.create(sender=sender, receiver=receiver, label=label, message=msg)
            ActivityLog.objects.create(person=user.person, time=now(), act="Message Sent")
            return HttpResponseRedirect('/messages/')

        if Patient.objects.filter(user=user).exists():
            return render(request, 'HNApp/patient/messages_create.html', {'form': form})
        if Doctor.objects.filter(user=user).exists():
            return render(request, 'HNApp/doctor/messages_create.html', {'form': form})

class MessageView(View):
    form_class = MessageForm
    template_name = 'HNApp/patient/messages_view.html'
    init = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        user = request.user
        my_message = Message.objects.get(id=next(iter(kwargs.values())))
        if my_message.receiver == user.person:
            my_message.message_read = True
            my_message.save()
        if Patient.objects.filter(user=user).exists():
            return render(request, 'HNApp/patient/messages_view.html', {'message': my_message,
                                                                        'today': localtime(now()).date()})
        if Doctor.objects.filter(user=user).exists():
            return render(request, 'HNApp/doctor/messages_view.html', {'message': my_message,
                                                                       'today': localtime(now()).date()})

    # This method is not used. I kept it just in case we need it. -Matt
    def post(self, request, *args, **kwargs):
        my_message = Message.objects.get(id=args)
        return render(request, self.template_name, {'message', my_message})

########## here begins the patients views ##########
@login_required()
def patients(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    patients = doctor.patients.all()
    return render(request, 'HNApp/doctor/view_patients.html', {'patients': patients})

class ViewPatientProfile(View):
    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(id=kwargs['pk'])
        appts = Appointment.objects.filter(patient=patient)
        up_appts = appts.filter(date__gt=localtime(now()).date())
        prev_appts = appts.filter(date__lt=localtime(now()).date())
        prescriptions = Prescription.objects.filter(patient=patient)
        medical_records = MedicalDocument.objects.filter(patient=patient)
        person = Person.objects.get(id=kwargs['pk'])
        phone_number = person.phone_number
        formatted_phone_number = "(" + phone_number[:3] + ") " + phone_number[3:6] + "-" + phone_number[6:10]
        patient = person.patient
        emg_number = patient.emg_contact_number
        formatted_emg_number = "(" + emg_number[:3] + ") " + emg_number[3:6] + "-" + emg_number[6:10]
        return render(request, 'HNApp/doctor/view_patient_profile.html', {'patient': patient,
                                                                          'up_appts': up_appts,
                                                                          'prev_appts': prev_appts,
                                                                          'prescriptions': prescriptions,
                                                                          'medical_records': medical_records,
                                                                          'formatted_phone_number': formatted_phone_number,
                                                                          'formatted_emg_number': formatted_emg_number})

class UploadPatientMedicalDoc(View):
    init = {'key': 'value'}
    form_class = UploadMedicalDocForm

    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(id=kwargs['pk'])
        #patient = [patient]
        form = self.form_class(initial=self.init)
        return render(request, 'HNApp/doctor/upload_medical_doc.html', {'form': form, 'patient': patient})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            patient = Patient.objects.get(id=kwargs['pk'])
            label = form.cleaned_data['label']
            file = request.FILES['upload']
            released = form.cleaned_data['released']
            MedicalDocument.objects.create(file=file, patient=patient, released=released, label=label)

            return HttpResponseRedirect("/patients/" + str(patient.id))

        return render(request, 'HNApp/doctor/upload_medical_doc.html', {'form': form})

class WritePatientPrescription(View):
    init = {'key': 'value'}
    form_class = WritePrescriptionForm

    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(id=kwargs['pk'])
        #patient = [patient]
        form = self.form_class(initial={'patient': patient})
        return render(request, 'HNApp/doctor/write_patient_prescription.html', {'form': form, 'patient': patient})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(id=kwargs['pk'])
            doctor = Doctor.objects.get(user=user)
            label = form.cleaned_data['label']
            amount = form.cleaned_data['amount']
            inst = form.cleaned_data['instructions']
            Prescription.objects.create(patient=patient, doctor=doctor, label=label, amount=amount, instructions=inst)
            return HttpResponseRedirect('/patients/' + str(patient.id))
        return HttpResponseRedirect('/messages/')

class ViewPatientPrescription(View):
    def get(self, request, *args, **kwargs):
        pres = Prescription.objects.get(id=kwargs['pk'])
        return render(request, 'HNApp/doctor/view_patient_prescription.html', {'pres': pres})

class ViewPatientAppointment(View):
    def get(self, request, *args, **kwargs):
        appt = Appointment.objects.get(id=kwargs['pk'])
        return render(request, 'HNApp/doctor/view_patient_appointment.html', {'appt': appt})


########## here begins other views ##########
@login_required()
def main_page(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'HNApp/main_page_admin.html')
    person = user.person
    phone_number = person.phone_number
    formatted_phone_number = "(" + phone_number[:3] + ") " + phone_number[3:6] + "-" + phone_number[6:10]
    if Patient.objects.filter(user=user).exists():
        patient = person.patient
        emg_number = patient.emg_contact_number
        formatted_emg_number = "(" + emg_number[:3] + ") " + emg_number[3:6] + "-" + emg_number[6:10]
        return render(request, 'HNApp/patient/main_page_patient.html', {'formatted_phone_number': formatted_phone_number,
                                                                        'formatted_emg_number': formatted_emg_number})
    if Doctor.objects.filter(user=user).exists():
        return render(request, 'HNApp/doctor/main_page_doctor.html', {'formatted_phone_number':formatted_phone_number})
    else:
        return render(request, 'HNApp/main_page.html')

class EditProfile(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        person = Person.objects.get(user=user)
        email = user.email
        first_name = user.first_name
        last_name = user.last_name
        phone_number = person.phone_number
        date_of_birth = person.date_of_birth
        address = person.address
        #sex = patient.sex
        #age = patient.age
       # weight = patient.weight
        #known_allergies = patient.known_allergies
        if Patient.objects.filter(user=user).exists():
            patient = Patient.objects.get(user=user)
            emg_contact_name = patient.emg_contact_name
            emg_contact_number = patient.emg_contact_number
            insurance_name = patient.insurance_name
            sex = patient.sex
            age = patient.age
            weight = patient.weight
            height = patient.height
            hospital = patient.hospital
            known_allergies = patient.known_allergies
            form = EditProfileFormPatient(initial={'email': email, 'first_name': first_name, 'last_name': last_name,
                                            'phone_number': phone_number, 'date_of_birth': date_of_birth, 'address':address,
                                            'emg_contact_name': emg_contact_name, 'emg_contact_number': emg_contact_number,
                                            'insurance_name': insurance_name, 'sex': sex, 'age': age, 'weight': weight,
                                            'height':height,'hospital':hospital, 'known_allergies': known_allergies})
            return render(request, 'HNApp/patient/edit_profile_patient.html', {'form': form})
        
        if Doctor.objects.filter(user=user).exists():
            form = EditProfileFormDoctor(initial={'email': email, 'first_name': first_name, 'last_name': last_name,
                                            'phone_number': phone_number, 'date_of_birth': date_of_birth, 'address':address})
            return render(request, 'HNApp/doctor/edit_profile_doctor.html', {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        if Patient.objects.filter(user=user).exists():
            form = EditProfileFormPatient(request.POST)
        if Doctor.objects.filter(user=user).exists():
            form = EditProfileFormDoctor(request.POST)
        if form.is_valid():
            person = Person.objects.get(user=user)
            #fetches cleaned data
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            name = first_name + ' ' + last_name
            phone_number = request.POST['phone_number']
            date_of_birth = form.cleaned_data['date_of_birth']
            address = request.POST['address']
            #sex=request.POST['sex']
            #age=request.POST['age']
            #weight=request.POST['weight']
            #known_allergies=request.POST['known_allergies']
            
            #updates information in models
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            person.name = name
            person.phone_number = phone_number
            person.date_of_birth = date_of_birth
            person.address = address
            #person.sex=sex
            #person.age=age
            #person.weight=weight
            #person.known_allergies=known_allergies
            user.save()
            person.save()
            ActivityLog.objects.create(person=user.person, time=now(), act="Update Profile")
            #fetches and updates patient specific information
            if Patient.objects.filter(user=user).exists():
                patient = Patient.objects.get(user=user)
                #fetch
                emg_contact_name = request.POST['emg_contact_name']
                emg_contact_number = request.POST['emg_contact_number']
                insurance_name = request.POST['insurance_name']
                sex=request.POST['sex']
                age=request.POST['age']
                weight=request.POST['weight']
                height=request.POST['height']
                hospital=request.POST['hospital']
                known_allergies=request.POST['known_allergies']
                #update
                patient.sex=sex
                patient.age=age
                patient.weight=weight
                patient.height=height
                patient.known_allergies=known_allergies
                patient.emg_contact_name = emg_contact_name
                patient.emg_contact_number = emg_contact_number
                patient.insurance_name = insurance_name
                patient.hospital=Hospital.objects.get(id=hospital)
                patient.save()
            return HttpResponseRedirect('/')
        if Patient.objects.filter(user=user).exists():
            return render(request, 'HNApp/patient/edit_profile_patient.html', {'form': form})
        if Doctor.objects.filter(user=user).exists():
            return render(request, 'HNApp/doctor/edit_profile_doctor.html', {'form': form})
        return HttpResponseRedirect('/appointments/')

def register_success(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        name = first_name + ' ' + last_name
        phone_number = request.POST['phone_number']
        date_of_birth = form.cleaned_data['date_of_birth']
        emg_contact_name = request.POST['emg_contact_name']
        emg_contact_number = request.POST['emg_contact_number']
        insurance_name = request.POST['insurance_name']
        user = User.objects.create_user(username=username, password=password,
                                        email=email, first_name=first_name, last_name=last_name)
        patient = Patient.objects.create(user=user, phone_number=phone_number, date_of_birth=date_of_birth,
                                                 emg_contact_name=emg_contact_name, name=name,
                                                 emg_contact_number=emg_contact_number,
                                                 insurance_name=insurance_name)
        ActivityLog.objects.create(person=user.person, time=now(), act="Register Account")
        # should really auto log in the user here but I cant get it to work
        #url = reverse('login', kwargs={'success': True})
        #return HttpResponseRedirect(url)
        form = AuthenticationForm()
        return render(request, 'HNApp/login.html', {'form': form, 'msg': 'Register success! Please log in:'})
    else:

        return render(request, 'HNApp/register.html', {'form': form})

def auth_log(request):
    form = AuthenticationForm(request.POST)
    if 1:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if Person.objects.filter(user=user).exists():
            ActivityLog.objects.create(person=user.person, time=now(), act="Login")
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user=user)
                if user.is_superuser:
                    return HttpResponseRedirect('/')
                return HttpResponseRedirect('/appointments/')
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

    return render(request, 'HNApp/login.html', {'form': form, 'msg': '*invalid username or password*'})

def login_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthenticationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthenticationForm()

    return render(request, 'HNApp/login.html', {'form': form, 'msg': 'Welcome, please log in:'})

def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'HNApp/register.html', {'form': form})

def stats(request):
    users = User.objects.all()
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'HNApp/statistics.html', {'users': users, 'patients': patients, 'doctors': doctors})

class ViewActivityLog(View):
    form_class = ViewActivityLogForm
    template_name = 'HNApp/ViewActivityLog.html'
    init = {'key': 'value'}

    ##generates page
    def get(self, request, *args, **kwargs):
        activities = ActivityLog.objects.all()
        form = self.form_class()

        return render(request, self.template_name, {'form': form, 'activities': activities})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        activities = ActivityLog.objects.all()
        if form.is_valid():
            if request.POST['name'] != "":
                name = request.POST['name']
                person = Person.objects.all().filter(name=name)
                activities = activities.filter(person=person)


        return render(request, self.template_name, {'form': form, 'activities': activities})

#class PatientSearch(autocomplete.Select2QuerySetView):
#    def get_queryset(self):
#        qs = Patient.objects.all()
#        if self.q:
#            qs = qs.filter(name__istartswith=self.q)
#        return qs
