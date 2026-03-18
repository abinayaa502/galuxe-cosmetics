import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'galuxe_project.settings')
django.setup()

from products.models import Product, Category, Brand

def seed_data():
    print("🧹 Cleaning old data...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    Brand.objects.all().delete()

    brands_list = ["MAC", "Nykaa", "L'Oreal", "Maybelline", "Estée Lauder", "Becca", "NARS", "Tarte", "GALUXE", "Beardo", "Nivea Men"]
    categories_dict = {
        "Lipstick": ["Matte", "Glossy", "Liquid", "Velvet"],
        "Foundation": ["HD", "Serum", "Full Coverage"],
        "Blush": ["Cream", "Tint", "Powder"],
        "Skincare": ["Serum", "Moisturizer", "Cleanser"],
        "Men": ["Beard Oil", "Face Wash", "Hair Wax", "Grooming Kit"]
    }

    # Create Category Objects
    cat_objs = {}
    for cat_name in categories_dict.keys():
        obj, _ = Category.objects.get_or_create(name=cat_name)
        cat_objs[cat_name] = obj

    # Create Brand Objects
    brand_objs = {}
    for b_name in brands_list:
        obj, _ = Brand.objects.get_or_create(name=b_name)
        brand_objs[b_name] = obj

    print("🌱 Seeding products...")
    for i in range(1, 61):
        brand_name = random.choice(brands_list)
        cat_key = random.choice(list(categories_dict.keys()))
        shade_suffix = random.choice(categories_dict[cat_key])
        
        gender = "Men" if cat_key == "Men" or "Men" in brand_name else "Women"
        
        name = f"{brand_name} {shade_suffix} {cat_key}"
        price = Decimal(random.randint(499, 4999))
        discount = random.choice([0, 5, 10, 15, 20, 30])
        rating = round(random.uniform(3.5, 5.0), 1)
        stock = random.randint(10, 100)
        
        Product.objects.create(
            name=name,
            brand_ref=brand_objs[brand_name],
            category_ref=cat_objs[cat_key],
            brand=brand_name,  # Legacy support
            category=cat_key,  # Legacy support
            gender=gender,
            price=price,
            discount=discount,
            rating=rating,
            description=f"Premium {cat_key} from {brand_name}. Designed for a luxury finish and lasting glow.",
            image="placeholder.jpg",
            stock=stock,
            is_trending=(i < 15)
        )

    print(f"✅ Success! Seeded {Product.objects.count()} products, {Category.objects.count()} categories, and {Brand.objects.count()} brands.")

if __name__ == "__main__":
    seed_data()
