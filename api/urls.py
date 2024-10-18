from django.urls import path
from .views import enroll

urlpatterns = [
    path('enroll/', enroll, name='enroll')
]