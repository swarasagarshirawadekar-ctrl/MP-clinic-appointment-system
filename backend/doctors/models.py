from django.db import models
from django.core.exceptions import ValidationError

class DoctorProfile(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    fee = models.IntegerField()

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Availability(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_length_minutes = models.IntegerField()

    def __str__(self):
        return f"{self.doctor.name} - {self.weekday}"


class Slot(models.Model):
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} {self.start_time} - {self.availability.doctor.name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.patient.name} - {self.slot}"

    def clean(self):
        # block booking if the slot is already taken by another appointment
        if self.slot.is_booked and not self.pk:
            raise ValidationError("This slot is already booked.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # a cancelled appointment frees the slot, any other status keeps it booked
        self.slot.is_booked = self.status != 'cancelled'
        self.slot.save()
    