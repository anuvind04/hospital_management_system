
from django import forms
from .models import booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = booking

        fields = [
            'patient_name',
            'patient_email',
            'patient_phone',
            'doctor_name',
            'booked_on',
            'appointment_time',
        ]

        labels = {
            'patient_name': 'Patient Name',
            'patient_email': 'Email',
            'patient_phone': 'Phone',
            'doctor_name': 'Select Doctor',
            'booked_on': 'Appointment Date',
            'appointment_time': 'Appointment Time',
        }

        widgets = {
            'patient_name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'form-control'
            }),

            'patient_email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control'
            }),

            'patient_phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone',
                'class': 'form-control'
            }),

            'doctor_name': forms.Select(attrs={
                'class': 'form-control'
            }),

            'booked_on': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'appointment_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
        }
