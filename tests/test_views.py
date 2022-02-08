from urllib import response
from django.test import RequestFactory, TestCase
import base64
from flask import request
from rest_framework import HTTP_HEADER_ENCODING, status
from rest_framework.test import APITestCase
from User.models import Doctors,Patients
from rest_framework.test import force_authenticate
from rest_framework.test import RequestsClient
from requests.auth import HTTPBasicAuth



class ViewsTestCase(APITestCase):
    
    def test_auth(self):
        response=self.client.get("http://127.0.0.1:8000/user/1")
        self.assertEqual(response,status_code=401)

