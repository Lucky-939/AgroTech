from django.urls import path
from .views import care_advisory

urlpatterns = [
    path('', care_advisory, name='care'),
]
