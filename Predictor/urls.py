
from django.urls import path,include
from . import views
urlpatterns = [
    path("<int:plant_id>/", views.predict_disease),
      path("crop-recomm/", views.crop_recommend, name="crop-recomm"),
    path("<int:plant_id>/", views.predict_disease, name="predict-disease"),
]