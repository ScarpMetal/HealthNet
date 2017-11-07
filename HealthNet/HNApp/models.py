import calendar

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

class Person(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    phone_number = models.CharField(max_length=12)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=50,default='')
    #sex=models .CharField(max_length=7,default='')
    #age=models.CharField(max_length=3,default='')
    #weight=models.CharField(max_length=3,default='')
    #known_allergies=models.CharField(max_length=200,default='')
    def __str__(self):
        return self.name

class Staff(Person):
    salary = models.IntegerField()
    #hours
    
class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=500)
    def __str__(self):
        return self.name

class Administration(Staff):
    def __str__(self):
        return self.name

class Nurse(Staff):
    def __str__(self):
        return self.name

class Patient(Person):
    emg_contact_name = models.CharField(max_length=30)
    emg_contact_number = models.CharField(max_length=10)
    insurance_name = models.CharField(max_length=30)
    #hospital = models.ForeignKey(Hospital, default='', blank=True, null=True, related_name = "admitted")
    sex=models .CharField(max_length=7,default='')
    age=models.CharField(max_length=3,default='')
    weight=models.CharField(max_length=3,default='')
    known_allergies=models.CharField(max_length=200,default='')
    height=models.CharField(max_length=3,default='')
    hospital = models.ForeignKey(Hospital, default=None, blank=True, null=True, related_name = "admitted")
    def get_last_appt(self):
        patient_appts = Appointment.objects.filter(patient=self).order_by('-date', '-time')
        return patient_appts[0].date
    def __str__(self):
        return self.name

class Doctor(Staff):
    patients = models.ManyToManyField(Patient)
    def __str__(self):
        return self.name

class MedicalDocument(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    label = models.CharField(max_length=30)
    file = models.FileField(upload_to='medicalDocs/')
    date = models.DateField()
    released = models.BooleanField(default=False)
    def __str__(self):
        return self.label

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    description = models.TextField(max_length=500)

    def get_absolute_url(self):
        return reverse('appointments')

    def __str__(self):
        return '%s -> Doctor %s (%s) [%s]' % (self.patient.name, self.doctor.name, self.date, self.time)

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    label = models.CharField(max_length=30)
    amount = models.IntegerField()
    date_prescribed = models.DateField(default=timezone.localtime(timezone.now()).date())
    instructions = models.TextField(max_length=500)

    def __str__(self):
        return self.label

class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="messages_sent")
    receiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="messages_received")
    date = models.DateField(default=timezone.localtime(timezone.now()).date())
    time = models.TimeField(default=timezone.localtime(timezone.now()))
    label = models.CharField(max_length=50)
    message = models.TextField()
    message_read = models.BooleanField(default=False)

    def month_as_str(self):
        return '%s' % (calendar.month_name[self.date.month])

    def __str__(self):
        return '%s -> %s  |  %s' % (self.sender.name, self.receiver.name, self.label)


class ActivityLog(models.Model):
    act = models.TextField(max_length=20)
    person = models.ForeignKey(Person)
    time = models.DateTimeField(default=timezone.localtime(timezone.now()).date())

    def __str__(self):
        return '%s at %s by %s' % (self.act, self.time, self.person.name)
