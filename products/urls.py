from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('women/', views.women_products, name='women_products'),
    path('men/', views.men_products, name='men_products'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]
