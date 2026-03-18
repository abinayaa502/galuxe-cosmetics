from django.urls import path
from . import views

urlpatterns = [
    path('', views.scanner_index, name='scanner_index'),
]
