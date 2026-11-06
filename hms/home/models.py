
from django.db import models
from django.contrib.auth.models import User


class dept(models.Model):
    dept_name = models.CharField(max_length=100)
    dept_desc = models.TextField()

    def __str__(self):
        return self.dept_name


class doctor(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='doctor_profile'
)
    doctor_name = models.CharField(max_length=100)
    doctor_specialisation = models.TextField()
    dept_name = models.ForeignKey(dept, on_delete=models.CASCADE)
    doctor_image = models.ImageField(
        upload_to='doctor_images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.doctor_name


class booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )

    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=15)

    doctor_name = models.ForeignKey(
        doctor,
        on_delete=models.CASCADE
    )

    booked_on = models.DateField()

    appointment_time = models.TimeField(default='09:00')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor_name}"


class profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
