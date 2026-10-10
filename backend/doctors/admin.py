from django.contrib import admin
from .models import DoctorProfile, Patient, Availability, Slot, Appointment

admin.site.register(DoctorProfile)
admin.site.register(Patient)
admin.site.register(Availability)
admin.site.register(Slot)
admin.site.register(Appointment)