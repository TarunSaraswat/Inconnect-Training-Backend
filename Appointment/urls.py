from xml.etree.ElementInclude import include
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('meetapi',views.MeetViewSet,basename='meet')
urlpatterns=[
    path('',views.Create_Appointment.as_view()),
    path('update/<int:pk>',views.GetUpdateMeet.as_view()),
    path('rating/<int:pk>',views.AddRating.as_view()),
    path('zipcode',views.Get_By_Zipcode.as_view()),
    path('',include(router.urls)),
]