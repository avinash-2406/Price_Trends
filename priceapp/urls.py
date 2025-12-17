from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_excel),
    path("price-trend/", views.price_trend),
    path("testentry/",views.testentry),
    path("getall_locations/",views.getall_locations)
]
