
from django.contrib import admin
from .models import booking, dept, doctor, profile


@admin.register(dept)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_name',)
    search_fields = ('dept_name',)


@admin.register(doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'doctor_name',
        'doctor_specialisation',
        'dept_name',
        'user'
    )

    list_filter = ('dept_name',)
    search_fields = ('doctor_name', 'doctor_specialisation')


@admin.register(booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name',
        'doctor_name',
        'booked_on',
        'appointment_time',
        'status'
    )

    list_filter = ('status', 'booked_on')
    search_fields = ('patient_name', 'patient_email')


@admin.register(profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')
