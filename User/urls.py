from django.urls import URLPattern
from django.urls import path
from . import views

urlpatterns=[
    path('<int:user_id>',views.getUpdateUser),
    path('',views.addUser)
]