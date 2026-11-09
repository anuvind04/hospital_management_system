
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('doctors/', views.doctors, name='doctors'),
    path('departments/', views.departments, name='departments'),

    path('booking/', views.booking, name='booking'),

    path(
        'booking/<int:doctor_id>/',
        views.booking,
        name='book_appointment'
    ),

    path(
        'patient-dashboard/',
        views.patient_dashboard,
        name='patient_dashboard'
    ),

    path(
        'cancel-appointment/<int:appointment_id>/',
        views.cancel_appointment,
        name='cancel_appointment'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('signup/', views.signup, name='signup'),

    path(
        'smart_recommendation/',
        views.smart_recommendation,
        name='smart_recommendation'
    ),
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),
        path(
        'doctor-dashboard/',
        views.doctor_dashboard,
        name='doctor_dashboard'
    ),
    path(
        'update-booking-status/<int:booking_id>/',
        views.update_booking_status,
        name='update_booking_status'
    ),
    
    path(
        'dashboard/patients/',
        views.admin_patients,
        name='admin_patients'
    ),

    path(
        'dashboard/doctors/',
        views.admin_doctors,
        name='admin_doctors'
    ),

    path(
        'dashboard/departments/',
        views.admin_departments,
        name='admin_departments'
    ),

    path(
        'dashboard/appointments/',
        views.admin_appointments,
        name='admin_appointments'
    ),

]
