from django.urls import path
from . import views

urlpatterns=[
    path('',views.Create_Appointment.as_view()),
    path('Update',views.Update_Meet.as_view()),
    path('rating',views.addRating),
    path('time',views.Get_By_Time.as_view()),
    path('service',views.Get_By_Service.as_view()),
    path('zipcode',views.Get_By_Zipcode.as_view())
]