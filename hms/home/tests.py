from django.test import TestCase

from .models import dept, doctor


class BookingViewTests(TestCase):
    def test_booking_page_renders(self):
        response = self.client.get('/booking/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book An Appointment')


class SmartRecommendationViewTests(TestCase):
    def test_smart_recommendation_page_renders(self):
        response = self.client.get('/smart_recommendation/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smart Doctor Recommendation')

    def test_recommended_doctor_has_preselected_booking_link(self):
        department = dept.objects.create(
            dept_name='Dermatology',
            dept_desc='Skin care',
        )
        recommended_doctor = doctor.objects.create(
            doctor_name='Dr. Example',
            doctor_specialisation='Dermatologist',
            dept_name=department,
        )

        response = self.client.post(
            '/smart_recommendation/',
            {'symptoms': 'skin rash'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="/booking/{recommended_doctor.pk}/"',
        )

    def test_booking_link_prefills_selected_doctor(self):
        department = dept.objects.create(
            dept_name='Dermatology',
            dept_desc='Skin care',
        )
        recommended_doctor = doctor.objects.create(
            doctor_name='Dr. Example',
            doctor_specialisation='Dermatologist',
            dept_name=department,
        )

        response = self.client.get(f'/booking/{recommended_doctor.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'<option value="{recommended_doctor.pk}" selected>',
            html=False,
        )

    def test_smart_recommendation_shows_matching_doctors(self):
        department = dept.objects.create(
            dept_name='Dermatology',
            dept_desc='Skin care',
        )
        doctor.objects.create(
            doctor_name='Dr. Example',
            doctor_specialisation='Dermatologist',
            dept_name=department,
        )

        response = self.client.post(
            '/smart_recommendation/',
            {'symptoms': 'skin rash'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Example')
        self.assertContains(response, 'Dermatologist')
