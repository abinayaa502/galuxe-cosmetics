from django.contrib import admin
from .models import Product, Category, Brand

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_ref', 'category_ref', 'price', 'discount', 'stock')
    list_filter = ('brand_ref', 'category_ref', 'gender', 'skin_type')
    search_fields = ('name', 'brand_ref__name', 'description')
    ordering = ('brand_ref', 'name')
