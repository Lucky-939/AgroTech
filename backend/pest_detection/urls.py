from django.urls import path
from . import views

urlpatterns = [
    path('', views.pest_detect_home, name='pest_detection_home'),
    path('api/pest-detect/', views.api_pest_detect, name='api_pest_detect'),
]
