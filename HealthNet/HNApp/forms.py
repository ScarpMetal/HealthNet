from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from HNApp.models import Hospital, Doctor, Patient, Person
#from dal import autocomplete
from django.forms.widgets import SelectDateWidget
from django.utils.timezone import localtime, now
from.models import Patient
gender_choices =(
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=10)
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(localtime(now()).year,1920,-1)))
    #doctors = forms.ModelMultipleChoiceField(queryset=Doctor.objects.all())
    emg_contact_name = forms.CharField(max_length=30)
    emg_contact_number = forms.CharField(max_length=10)
    insurance_name = forms.CharField(max_length=30)
    pass

class EditProfileFormPatient(forms.Form):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=10, required=False)
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(localtime(now()).year,1920,-1)))
    address = forms.CharField(max_length=50, required=False)
    emg_contact_name = forms.CharField(max_length=30)
    emg_contact_number = forms.CharField(max_length=10)
    insurance_name = forms.CharField(max_length=30)
    age = forms.CharField(max_length=3,required=False)
    weight = forms.CharField(max_length=3,required=False)
    sex = forms.ChoiceField(choices=gender_choices, required = False, widget=forms.Select(attrs={'class':'selectpicker form-control'}))
    #sex = forms.CharField(max_length=7,required=False)
    height = forms.CharField(max_length=3,required=False)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required = True, widget=forms.Select(attrs={'class':'selectpicker show-tick form-control'}),empty_label="none")
    known_allergies = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 50, 'rows': 4}))

class EditProfileFormDoctor(forms.Form):    
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=10, required=False)
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(localtime(now()).year,1920,-1)))
    address = forms.CharField(max_length=50, required=False)

class MessageForm(forms.Form):
    receiver = forms.ModelMultipleChoiceField(queryset=Person.objects.all().order_by('name'))
    label = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size': 48}))
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}))

class CreateAppointmentFormDoctor(forms.Form):
    patient = forms.ModelMultipleChoiceField(queryset=Patient.objects.all().order_by('name'))
    time = forms.TimeField()
    date = forms.DateField()
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}))

class CreateAppointmentFormPatient(forms.Form):
    doctor = forms.ModelMultipleChoiceField(queryset=Doctor.objects.all().order_by('name'))
    time = forms.TimeField()
    date = forms.DateField()
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}))

class UploadMedicalDocForm(forms.Form):
    label = forms.CharField(required=False)
    upload = forms.FileField()
    released = forms.BooleanField(required=False)

class WritePrescriptionForm(forms.Form):
    #patient = forms.ModelMultipleChoiceField(queryset=Patient.objects.all().order_by('name'))
    label = forms.CharField(max_length=30)
    amount = forms.IntegerField()
    instructions = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}))

class ViewActivityLogForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
#class TestForm(forms.ModelForm):
#   patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
#                                    widget=autocomplete.ModelSelect2(url='country-autocomplete'))
