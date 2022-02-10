from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Appointment import views

router = DefaultRouter()
router.register('meetapi', views.MeetViewSet, basename='meet')
urlpatterns = [
    path('rating/<int:pk>', views.AddRating.as_view()),
    path('zipcode', views.GetByZipcode.as_view()),
    path('', include(router.urls)),
]
