from django.urls import path
from .views import disease_home

urlpatterns = [
    path('', disease_home, name='disease'),
<<<<<<< HEAD
    path('<int:id>/', disease_home, name='disease_with_id'),
=======
>>>>>>> 05f56bc7 (Initial commit for AgroTech)
]
