from django.urls import path

from calculator import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/calc", views.calculate, name="calculate"),
    path("healthz", views.healthz, name="healthz"),
]
