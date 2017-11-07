from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Person)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(MedicalDocument)
admin.site.register(Message)
admin.site.register(Hospital)
