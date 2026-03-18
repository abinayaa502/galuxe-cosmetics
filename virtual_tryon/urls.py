from django.urls import path
from . import views

urlpatterns = [
    path('', views.tryon_index, name='tryon_index'),
]
