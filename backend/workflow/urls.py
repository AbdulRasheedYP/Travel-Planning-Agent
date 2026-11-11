from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
     path("generate-trip/", views.generate_trip, name="generate_trip"),

]