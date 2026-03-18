from django.shortcuts import render
from products.models import Product
from django.db.models import Q

def home(request):
    # Fetch sections for the redesigned homepage
    trending = Product.objects.filter(is_trending=True)[:4]
    if not trending.exists():
        trending = Product.objects.all().order_by('?')[:4]
        
    best_sellers = Product.objects.filter(is_best_seller=True)[:4]
    if not best_sellers.exists():
        best_sellers = Product.objects.all().order_by('-rating')[:4]
        
    new_arrivals = Product.objects.filter(is_new_arrival=True)[:4]
    if not new_arrivals.exists():
        new_arrivals = Product.objects.all().order_by('-id')[:4]

    collections = [
        {"title": "Trending Now", "subtitle": "Curated Selection", "products": trending, "filter": "trending=1"},
        {"title": "Best Sellers", "subtitle": "Highly Rated", "products": best_sellers, "filter": "best_seller=1"},
        {"title": "New Arrivals", "subtitle": "Just Landed", "products": new_arrivals, "filter": "new_arrival=1"},
    ]
    
    return render(request, 'homepage.html', {'collections': collections})
