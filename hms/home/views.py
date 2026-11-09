from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import dept, doctor, booking as Booking, profile as Profile
from .forms import BookingForm
from .recomendation import recommend_doctors
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone


@login_required
def index(request):
    numbers = {
        'num1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    return render(request, 'index.html', numbers)


def about(request):
    students = {
        "students": [
            "Anuvind", "shadhil", "aadhithyan",
            "Tenson", "vishnu", "soorya", "anagha"
        ]
    }
    return render(request, 'about.html', students)


def doctors(request):
    dict_doctors = {
        'doctors': doctor.objects.all()
    }
    return render(request, 'doctors.html', dict_doctors)


def departments(request):
    dict_dept = {
        'departments': dept.objects.all(),
        'doctor_count': doctor.objects.count()
    }
    return render(request, 'departments.html', dict_dept)


def contact(request):
    fruits = {
        'fruits': ['apple', 'banana', 'orange', 'grape', 'kiwi']
    }
    return render(request, 'contact.html', fruits)


@login_required
def booking(request, doctor_id=None):

    initial = {
        'patient_name': request.user.get_full_name() or request.user.username,
        'patient_email': request.user.email,
    }

    try:
        patient_profile = Profile.objects.get(user=request.user)
        initial['patient_phone'] = patient_profile.phone_number
    except Profile.DoesNotExist:
        pass

    if doctor_id is not None:
        initial["doctor_name"] = get_object_or_404(
            doctor,
            pk=doctor_id
        )

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            return redirect('patient_dashboard')

    else:
        form = BookingForm(initial=initial)

    return render(request, "Booking.html", {"form": form})



@login_required
def patient_dashboard(request):
    patient_profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    appointments = Booking.objects.filter(
        user=request.user
    ).select_related(
        'doctor_name',
        'doctor_name__dept_name'
    ).order_by('-created_at')

    context = {
        'patient_profile': patient_profile,
        'appointments': appointments,

        'total_appointments': appointments.count(),
        'pending_appointments': appointments.filter(
            status='Pending'
        ).count(),
        'approved_appointments': appointments.filter(
            status='Approved'
        ).count(),
        'rejected_appointments': appointments.filter(
            status='Rejected'
        ).count(),
        'completed_appointments': appointments.filter(
            status='Completed'
        ).count(),
        'cancelled_appointments': appointments.filter(
            status='Cancelled'
        ).count(),
    }

    return render(
        request,
        'patient_dashboard.html',
        context
    )

@login_required
@require_POST
def cancel_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Booking,
        id=appointment_id,
        user=request.user
    )

    if appointment.status in ['Pending', 'Approved']:
        appointment.status = 'Cancelled'
        appointment.save(update_fields=['status'])

    return redirect('patient_dashboard')


def signup(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('patient_dashboard')

    else:
        form = UserCreationForm()

    return render(
        request,
        "signup.html",
        {"form": form}
    )


def smart_recommendation(request):

    doctors_list = []
    symptoms = ""
    searched = False

    if request.method == "POST":
        symptoms = request.POST.get(
            "symptoms", ""
        ).strip()

        searched = True

        if symptoms:
            doctors_list = recommend_doctors(symptoms)

    return render(
        request,
        "smart_recomendation.html",
        {
            "doctors": doctors_list,
            "symptoms": symptoms,
            "searched": searched,
        }
    )

@login_required(login_url='login')
def dashboard(request):

    # Hospital-wide stats are for staff only; patients use their own dashboard
    if not request.user.is_staff:
        return redirect('patient_dashboard')

    today = timezone.localdate()

    bookings = Booking.objects.select_related(
        'doctor_name',
        'doctor_name__dept_name'
    )

    status_counts = {
        status: bookings.filter(status=status).count()
        for status, _ in Booking.STATUS_CHOICES
    }

    context = {
        "total_doctors": doctor.objects.count(),
        "total_departments": dept.objects.count(),
        "total_patients": Profile.objects.filter(
    user__is_staff=False,
    user__is_superuser=False
).exclude(
    user__doctor_profile__isnull=False
).count(),
        "total_appointments": bookings.count(),
        "pending_appointments": status_counts['Pending'],
        "status_counts": status_counts,
        "today_appointments": bookings.filter(
            booked_on=today
        ).order_by('appointment_time'),
        "top_doctors": doctor.objects.select_related(
            'dept_name'
        ).annotate(
            total=Count('booking')
        ).order_by('-total')[:5],
        "recent_bookings": bookings.order_by('-created_at')[:10],
    }

    return render(request, "home/dashboard.html", context)
STATUS_TRANSITIONS = {
    'Pending': ['Approved', 'Rejected'],
    'Approved': ['Completed', 'Rejected'],
}


# Staff-only patient list
@login_required(login_url='login')
def admin_patients(request):
    if not request.user.is_staff:
        return redirect('patient_dashboard')

    search = request.GET.get('q', '').strip()

    patients = Profile.objects.select_related('user').filter(
        user__is_staff=False,
        user__is_superuser=False
    ).exclude(
        user__doctor_profile__isnull=False
    )

    if search:
        patients = patients.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(address__icontains=search)
        )

    return render(request, 'home/records_list.html', {
        'page_title': 'Patients',
        'page_type': 'patients',
        'records': patients.order_by('user__username'),
        'search': search,
    })


# Staff-only doctor list
@login_required(login_url='login')
def admin_doctors(request):
    if not request.user.is_staff:
        return redirect('patient_dashboard')

    search = request.GET.get('q', '').strip()

    doctors_list = doctor.objects.select_related('dept_name')

    if search:
        doctors_list = doctors_list.filter(
            Q(doctor_name__icontains=search) |
            Q(doctor_specialisation__icontains=search) |
            Q(dept_name__dept_name__icontains=search)
        )

    return render(request, 'home/records_list.html', {
        'page_title': 'Doctors',
        'page_type': 'doctors',
        'records': doctors_list.order_by('doctor_name'),
        'search': search,
    })


# Staff-only department list
@login_required(login_url='login')
def admin_departments(request):
    if not request.user.is_staff:
        return redirect('patient_dashboard')

    search = request.GET.get('q', '').strip()

    departments_list = dept.objects.annotate(
        total_doctors=Count('doctor', distinct=True)
    )

    if search:
        departments_list = departments_list.filter(
            dept_name__icontains=search
        )

    return render(request, 'home/records_list.html', {
        'page_title': 'Departments',
        'page_type': 'departments',
        'records': departments_list.order_by('dept_name'),
        'search': search,
    })


# Staff-only appointment list
@login_required(login_url='login')
def admin_appointments(request):
    if not request.user.is_staff:
        return redirect('patient_dashboard')

    search = request.GET.get('q', '').strip()
    selected_status = request.GET.get('status', '').strip()

    appointments = Booking.objects.select_related(
        'doctor_name',
        'doctor_name__dept_name',
        'user'
    )

    if search:
        appointments = appointments.filter(
            Q(patient_name__icontains=search) |
            Q(patient_email__icontains=search) |
            Q(patient_phone__icontains=search) |
            Q(doctor_name__doctor_name__icontains=search)
        )

    if selected_status in dict(Booking.STATUS_CHOICES):
        appointments = appointments.filter(status=selected_status)

    return render(request, 'home/records_list.html', {
        'page_title': 'Appointments',
        'page_type': 'appointments',
        'records': appointments.order_by('-booked_on', '-appointment_time'),
        'search': search,
        'selected_status': selected_status,
        'status_choices': Booking.STATUS_CHOICES,
    })



@login_required(login_url='login')
def doctor_dashboard(request):

    doctor_obj = getattr(request.user, 'doctor_profile', None)

    # Only users linked to a doctor can open this page
    if doctor_obj is None:
        return redirect('index')

    all_appointments = Booking.objects.filter(
        doctor_name=doctor_obj
    )

    appointments = all_appointments.order_by(
        '-booked_on', '-appointment_time'
    )

    status_filter = request.GET.get('status', '')
    if status_filter in dict(Booking.STATUS_CHOICES):
        appointments = appointments.filter(status=status_filter)

    today = timezone.localdate()

    context = {
        'doctor': doctor_obj,
        'appointments': appointments,
        'status_filter': status_filter,
        'status_choices': [s for s, _ in Booking.STATUS_CHOICES],
        'total_appointments': all_appointments.count(),
        'pending_appointments': all_appointments.filter(status='Pending').count(),
        'today_appointments': all_appointments.filter(
            booked_on=today
        ).exclude(status__in=['Rejected', 'Cancelled']).count(),
        'completed_appointments': all_appointments.filter(status='Completed').count(),
    }

    return render(request, 'home/doctor_dashboard.html', context)


@login_required(login_url='login')
@require_POST
def update_booking_status(request, booking_id):

    doctor_obj = getattr(request.user, 'doctor_profile', None)

    if doctor_obj is None:
        return redirect('index')

    # A doctor can only change their own bookings
    appointment = get_object_or_404(
        Booking,
        id=booking_id,
        doctor_name=doctor_obj
    )

    new_status = request.POST.get('status')

    if new_status in STATUS_TRANSITIONS.get(appointment.status, []):
        appointment.status = new_status
        appointment.save(update_fields=['status'])

    return redirect('doctor_dashboard')
