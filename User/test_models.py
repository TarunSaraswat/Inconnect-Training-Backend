import unittest
from django.test import TestCase
from User.models import Doctors, Patients


class BaseModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        cls.doctor_one = Doctors(email="Saqnjeev@gmail.com", name="Sanjeev Rathore", city="Lucknow",
                                 state="Uttar Pradesh", zipcode="204101")
        cls.doctor_one.save()
        cls.doctor_two = Doctors(email="tarun@gmail.com", name="Tarun", city="Lucknow", state="Uttar Pradesh",
                                 zipcode="204101")
        cls.doctor_two.save()
        cls.patient_one = Patients(email="tarun@gmail.com", name="Tarun", city="Lucknow", state="Uttar Pradesh",
                                   zipcode="204101")
        cls.patient_one.save()
        cls.patient_two = Patients(email="Saqnjeev@gmail.com", name="Sanjeev Rathore", city="Lucknow",
                                   state="Uttar Pradesh", zipcode="204101")
        cls.patient_two.save()


class PatientModelTestCase(BaseModelTestCase):
    def test_patient_one_created_properly(self):
        self.assertEqual(True, self.patient_one in Patients.objects.all())

    def test_patient_two_created_properly(self):
        self.assertEqual(True, self.patient_two in Patients.objects.all())


class DoctorModelTestCase(BaseModelTestCase):
    def test_doctor_one_created_properly(self):
        self.assertEqual(True, self.doctor_one in Doctors.objects.all())

    def test_doctor_two_created_properly(self):
        self.assertEqual(True, self.doctor_two in Doctors.objects.all())


class PatientFailModelTestCase(TestCase):
    @unittest.expectedFailure
    def test_fail_patient_insertion_one(self):
        """giving only one field in patients"""
        patient_fail = Patients(email="Saqnjeev@gmail.com")
        patient_fail.save()

    @unittest.expectedFailure
    def test_fail_patient_insertion_two(self):
        """
        zipcode field missing in patients object
        """
        patient_fail = Patients(email="Saqnjeev@gmail.com", name="Sanjeev Rathore", city="Lucknow",
                                state="Uttar Pradesh")
        patient_fail.save()


class DoctorFailModelTestCase(TestCase):
    @unittest.expectedFailure
    def test_fail_doctor_insertion_one(self):
        """
        giving only one field in doctors
        """
        doctor_fail = Doctors(email="Saqnjeev@gmail.com")
        doctor_fail.save()

    @unittest.expectedFailure
    def test_fail_doctor_insertion_two(self):
        """
        zipcode field missing in doctors object
        """
        doctor_fail = Doctors(email="Saqnjeev@gmail.com", name="Sanjeev Rathore", city="Lucknow", state="Uttar Pradesh")
        doctor_fail.save()
