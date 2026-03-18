import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'galuxe_project.settings')
django.setup()

from products.models import Product

def seed_data():
    brands = ["GALUXE", "Nykaa", "MAC", "L'Oreal", "Maybelline", "Estée Lauder", "Becca", "NARS", "Tarte"]
    categories = {
        "Lipstick": ["Matte", "Glossy", "Liquid", "Bullet", "Velvet"],
        "Foundation": ["Full Coverage", "Light", "HD", "Serum", "Stick"],
        "Blush": ["Cream", "Powder", "Tint", "Shimmer"],
        "Skincare": ["Serum", "Moisturizer", "Cleanser", "Sunscreen"],
        "Men": ["Beard Oil", "Face Wash", "Hair Wax", "Perfume", "Grooming Kit"]
    }
    
    # Generic URLs for cosmetics (using unsplash IDs)
    female_cosmetics_images = [
        "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=400",
        "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=400",
        "https://images.unsplash.com/photo-1596462502278-27bfdc4033c8?auto=format&fit=crop&w=400",
        "https://images.unsplash.com/photo-1515688598190-8292788339c3?auto=format&fit=crop&w=400"
    ]
    
    male_cosmetics_images = [
        "https://images.unsplash.com/photo-1552046122-03184de8560c?auto=format&fit=crop&w=400",
        "https://images.unsplash.com/photo-1621607512214-68297480165e?auto=format&fit=crop&w=400",
        "https://images.unsplash.com/photo-1590666270543-9cc2d5257f86?auto=format&fit=crop&w=400"
    ]

    print("Seeding 50+ products...")
    for i in range(1, 61):
        brand = random.choice(brands)
        cat_key = random.choice(list(categories.keys()))
        shade_suffix = random.choice(categories[cat_key])
        
        gender = "Men" if cat_key == "Men" else "Women"
        image_url = random.choice(male_cosmetics_images if gender == "Men" else female_cosmetics_images)
        
        name = f"{brand} {shade_suffix} {cat_key}"
        price = Decimal(random.randint(499, 4999))
        discount = random.randint(5, 40)
        rating = round(random.uniform(3.5, 5.0), 1)
        stock = random.randint(10, 100)
        shade = f"Shade {random.randint(100, 999)}" if cat_key != "Skincare" else None
        
        # In a real app we'd download the image. Here we use a trick to make it work with ImageField
        # by creating a dummy record or just using the URL (but our model uses ImageField).
        # For this demo, I'll use a script that just creates the entries.
        # Note: ImageField expects a file. I'll use a hack by setting path if I can't download.
        # Better: let's just use a placeholder string or skip the ImageField requirement for now by allowing null.
        
        Product.objects.create(
            name=name,
            brand=brand,
            category=cat_key,
            gender=gender,
            price=price,
            discount=discount,
            rating=rating,
            description=f"Luxury {cat_key} from {brand}. Perfect for enhancing your beauty and glow.",
            image="placeholder.jpg", # We'll need a placeholder file
            stock=stock,
            shade=shade
        )

    print("Success!")

if __name__ == "__main__":
    seed_data()
