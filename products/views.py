from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Brand, Category

def get_product_context(request, queryset, **extra_context):
    search = request.GET.get('search')
    brand_name = request.GET.get('brand')
    category_name = request.GET.get('category')
    gender = request.GET.get('gender')
    skin_type = request.GET.get('skin_type')
    
    products = queryset
    
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(brand_ref__name__icontains=search) | 
            Q(category_ref__name__icontains=search) |
            Q(description__icontains=search)
        )
    if brand_name:
        products = products.filter(Q(brand_ref__name=brand_name) | Q(brand=brand_name))
    if category_name:
        products = products.filter(Q(category_ref__name=category_name) | Q(category=category_name))
    if gender:
        products = products.filter(gender=gender)
    if skin_type:
        products = products.filter(skin_type=skin_type)
        
    # Dynamic sidebar options based on current collection
    brands = Brand.objects.filter(products__id__in=queryset.values_list('id', flat=True)).values_list('name', flat=True).distinct().order_by('name')
    categories = Category.objects.filter(products__id__in=queryset.values_list('id', flat=True)).values_list('name', flat=True).distinct().order_by('name')
    skin_types = queryset.values_list('skin_type', flat=True).distinct().order_by('skin_type')
    
    context = {
        'products': products.select_related('brand_ref', 'category_ref'),
        'brands': brands,
        'categories': categories,
        'skin_types': skin_types,
        'current_gender': gender,
        'current_category': category_name,
        'current_brand': brand_name,
        'current_skin_type': skin_type
    }
    context.update(extra_context)
    return context

def product_list(request):
    ctx = get_product_context(request, Product.objects.all())
    return render(request, 'products/product_list.html', ctx)

def women_products(request):
    ctx = get_product_context(request, Product.objects.filter(gender='Women'), current_gender='Women')
    return render(request, 'products/product_list.html', ctx)

def men_products(request):
    ctx = get_product_context(request, Product.objects.filter(gender='Men'), current_gender='Men')
    return render(request, 'products/product_list.html', ctx)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
