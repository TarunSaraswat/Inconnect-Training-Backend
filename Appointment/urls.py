from xml.etree.ElementInclude import include
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('meetapi',views.MeetViewSet,basename='meet')
urlpatterns=[
    path('',views.CreateAppointment.as_view()),
    # path('update/<int:pk>',views.GetUpdateMeet.as_view()),
    path('rating/<int:pk>',views.AddRating.as_view()),
    path('zipcode',views.GetByZipcode.as_view()),
    path('',include(router.urls)),
]