from django.test import tag
from rest_framework.test import APITestCase
from User.models import Doctors
from django.contrib.auth.models import User


@tag('doctorViewSet')
class DoctorViewsetTest(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        Doctors.objects.create(email="Saqnjeev@gmail.com", name="Sanjeev Rathore", city="Lucknow",
                               state="Uttar Pradesh", zipcode="204101")
        Doctors.objects.create(email="Rahul@gmail.com", name="Rahul", city="Ghaziabad",
                               state="Uttar Pradesh", zipcode="201206")
        password = 'Tarun@innovaccer@1998'
        User.objects.create_superuser('myuser', password)

    def test_view_url_exists_at_desired_location(self):
        my_admin = User.objects.get(is_superuser=True)
        self.client.force_login(user=my_admin)
        response = self.client.get('/user/doctorapi/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_undesired_location(self):
        """
        since there are 2 doctors, there should be an error accessing third doctor
        """
        with self.assertRaises(AssertionError):
            my_admin = User.objects.get(is_superuser=True)
            self.client.force_login(user=my_admin)
            response = self.client.get('/user/doctorapi/3')
            self.assertEqual(response.status_code, 200)

        self.assertEqual(response.status_code, 404)

    def test_view_url_posts_at_desired_location(self):
        my_admin = User.objects.get(is_superuser=True)
        self.client.force_login(user=my_admin)
        data = {
            "email": "Shruti@gmail.com",
            "name": "Doctor Shruti",
            "city": "city",
            "state": "state",
            "zipcode": "204101"
        }
        response = self.client.post('/user/doctorapi', data)
        self.assertEqual(response.status_code, 201)

    def test_view_url_posts_wrong_data(self):
        """
        Posting invalid email to check validation
        """
        with self.assertRaises(AssertionError):
            my_admin = User.objects.get(is_superuser=True)
            self.client.force_login(user=my_admin)
            data = {
                "email": "email.com",
                "name": "Doctor Shruti",
                "city": "city",
                "state": "state",
                "zipcode": "204101"
            }
            response = self.client.post('/user/doctorapi', data)
            self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_code, 400)
