from django.urls import URLPattern
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

urlpatterns=[
    path('<int:user_id>',views.Get_Update_Patient.as_view()),
    path('doctor',views.Register_Doctor.as_view()),
    path('patient',views.Register_Patient.as_view())
]