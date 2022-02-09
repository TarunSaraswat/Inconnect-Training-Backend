from django.urls import path, include
from User import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('patientapi', views.PatientViewSet, basename='patient')
router.register('doctorapi', views.DoctorViewSet, basename='doctor')

urlpatterns = [
    path('', include(router.urls)),
]
