from django.urls import path
from . import views

urlpatterns=[
    path('get/',views.getAppointmentPatient),
    path('',views.createAppointment),
    path('updateTime',views.updateMeet),
    path('rating',views.addRating),
    path('time',views.getAppointmentByTime),
    path('service',views.getAppointmentByService),
    path('zipcode',views.getAppointmentByZipcode)
]