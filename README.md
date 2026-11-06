# Hospital Management System

A Django web application for browsing hospital doctors and departments, requesting appointments, and managing appointments through patient, doctor, and staff dashboards.

## Features

- Browse doctors and departments.
- Create an account and request appointments with a selected doctor and date/time.
- View and cancel eligible appointments from the patient dashboard.
- Review and update assigned appointments from a doctor dashboard.
- View hospital-wide appointment and clinic statistics from the staff dashboard.
- Get informational doctor suggestions from a symptom-to-specialty keyword matcher.
- Manage clinic records through Django admin.

The recommendation feature is informational only and does not diagnose medical conditions. Seek urgent medical care for emergency symptoms.

## Requirements

- Python 3.14.3 (the version used by the included Dockerfile)
- Packages listed in `hms/requirements.txt`

The requirements pin Django 6.1.2 and Pillow 12.3.0. If Python 3.14 is unavailable, use a Python version supported by the installed Django release and dependencies.

## Run locally on Windows

Open PowerShell in the repository directory:

```powershell
cd hms
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. The app uses SQLite by default, stored in `hms/db.sqlite3`; uploaded media is stored in `hms/media/`.

To create a staff account for Django admin and the staff dashboard:

```powershell
python manage.py createsuperuser
```

Optionally, populate the database with sample departments, doctors, and synthetic appointment records:

```powershell
python seed_clinic_data.py
```

## Pages

| Page | URL | Access |
| --- | --- | --- |
| Home | `/` | Login required |
| About | `/about/` | Public |
| Contact | `/contact/` | Public |
| Doctors | `/doctors/` | Public |
| Departments | `/departments/` | Public |
| Appointment booking | `/booking/` | Login required |
| Book with a selected doctor | `/booking/<doctor_id>/` | Login required |
| Patient dashboard | `/patient-dashboard/` | Login required |
| Smart doctor recommendation | `/smart_recommendation/` | Public |
| Sign up | `/signup/` | Public |
| Login / logout | `/login/`, `/logout/` | Public |
| Doctor dashboard | `/doctor-dashboard/` | Login as a user linked to a doctor |
| Staff dashboard | `/dashboard/` | Staff login required |
| Django admin | `/admin/` | Staff login required |

Doctors can move appointments through the available statuses from their dashboard. Patients can cancel pending or approved appointments from theirs.

## Run tests

From the `hms` directory:

```powershell
python manage.py test home.tests
```

## Project layout

```text
hms/
  hms/                 Django project settings and root URLs
  home/                Application models, views, forms, and routes
    templates/          HTML templates
    static/css/         Site styles
    recomendation.py    Symptom-to-specialty recommendation rules
  media/                Uploaded profile and doctor images
  manage.py
  requirements.txt
  seed_clinic_data.py   Optional synthetic clinic data
  Dockerfile
```

## Docker

The Dockerfile is in `hms/`. From that directory, build and run the development container:

```powershell
docker build -t hospital-management-system .
docker run --rm -p 8000:8000 hospital-management-system
```

The container starts Django's development server. Before deploying publicly, configure production settings, including a secret key, `DEBUG`, allowed hosts, database, and static/media file serving.
