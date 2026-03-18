import os
import django
import random
import requests
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'galuxe_project.settings')
django.setup()

from products.models import Product, Category, Brand

def download_image(url, filename):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            media_path = Path("media/products")
            media_path.mkdir(parents=True, exist_ok=True)
            with open(media_path / filename, 'wb') as f:
                f.write(response.content)
            return f"products/{filename}"
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

def seed_v3():
    print("Clearing existing data...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    Brand.objects.all().delete()

    CATEGORIES_CONFIG = {
        'Women': {
            'Lipstick': 'lipstick+makeup',
            'Foundation': 'foundation+cosmetics',
            'Mascara': 'mascara+eyes',
            'Eyeshadow': 'eyeshadow+palette',
            'Perfume': 'perfume+bottle+luxury',
            'Moisturizer': 'skincare+cream',
            'Face Wash': 'face+wash+skincare',
            'Nail Polish': 'nail+polish+luxury',
            'Serum': 'serum+skincare+bottle'
        },
        'Men': {
            'Beard Oil': 'beard+oil+men',
            'Shaving Cream': 'shaving+cream+men',
            'Perfume': 'men+fragrance+luxury',
            'Face Wash': 'men+face+wash',
            'Hair oil': 'men+hair+oil',
            'Body Spray': 'men+deodorant'
        }
    }

    BRANDS_CONFIG = {
        'Women': ['MAC', 'Estée Lauder', 'Lakmé', 'Maybelline', 'L\'Oréal', 'Nykaa', 'Forest Essentials', 'Huda Beauty'],
        'Men': ['Beardo', 'The Man Company', 'Ustraa', 'Philips', 'Gillette', 'Park Avenue', 'Old Spice', 'Nivea Men']
    }

    SHADES = {
        'Lipstick': ['Ruby Red', 'Wine Red', 'Nude Pink', 'Rose Pink', 'Coral Orange', 'Deep Plum'],
        'Foundation': ['Ivory', 'Beige', 'Sand', 'Honey', 'Caramel', 'Mocha'],
        'Nail Polish': ['Crimson', 'Petal Pink', 'Midnight Black', 'Gold Shimmer'],
    }

    # Create Categories
    category_objs = {}
    for gender_cats in CATEGORIES_CONFIG.values():
        for cat_name in gender_cats.keys():
            if cat_name not in category_objs:
                obj, _ = Category.objects.get_or_create(name=cat_name)
                category_objs[cat_name] = obj

    # Create Brands
    brand_objs = {}
    for gender_brands in BRANDS_CONFIG.values():
        for brand_name in gender_brands:
            if brand_name not in brand_objs:
                obj, _ = Brand.objects.get_or_create(name=brand_name)
                brand_objs[brand_name] = obj

    print("Downloading pool of high-quality images...")
    image_pool = {}
    for gender, cats in CATEGORIES_CONFIG.items():
        for cat, keyword in cats.items():
            pool = []
            # Download 3 unique images per category
            for i in range(3):
                url = f"https://source.unsplash.com/featured/800x800?{keyword}&sig={random.randint(1, 10000)}"
                filename = f"{cat.lower().replace(' ', '_')}_{i}.jpg"
                local_path = download_image(url, filename)
                if local_path:
                    pool.append(local_path)
            image_pool[cat] = pool

    print("Seeding products...")
    products_to_create = []
    
    # Generate 200 products
    for i in range(200):
        gender = random.choice(['Women', 'Men'])
        cat_name = random.choice(list(CATEGORIES_CONFIG[gender].keys()))
        brand_name = random.choice(BRANDS_CONFIG[gender])
        
        category = category_objs[cat_name]
        brand = brand_objs[brand_name]
        
        shade = None
        current_name = f"{brand_name} {cat_name}"
        if cat_name in SHADES:
            shade = random.choice(SHADES[cat_name])
            current_name += f" - {shade}"
        
        current_name += f" {'Elite' if i % 2 == 0 else 'Premium'}"
        
        price = random.randint(199, 1499)
        discount = random.choice([0, 10, 15, 20, 25, 40])
        rating = round(random.uniform(3.8, 5.0), 1)
        skin_type = random.choice(['All', 'Oily', 'Dry', 'Combination', 'Sensitive'])
        
        description = f"Experience the luxury of {brand_name}. This premium {cat_name} is curated to provide professional results. Perfect for {skin_type} skin types."
        
        # Pick from pool if available, otherwise use external
        image_path = None
        if cat_name in image_pool and image_pool[cat_name]:
            image_path = random.choice(image_pool[cat_name])
        
        product = Product(
            name=current_name,
            brand_ref=brand,
            category_ref=category,
            gender=gender,
            price=price,
            discount=discount,
            rating=rating,
            description=description,
            image=image_path,
            image_external_url=f"https://source.unsplash.com/featured/800x800?{CATEGORIES_CONFIG[gender][cat_name]}&sig={i}" if not image_path else "",
            stock=random.randint(10, 100),
            shade=shade,
            skin_type=skin_type,
            is_trending=(i < 20),
            is_best_seller=(30 < i < 50),
            is_new_arrival=(60 < i < 80)
        )
        products_to_create.append(product)

    Product.objects.bulk_create(products_to_create)
    print(f"Successfully seeded {Product.objects.count()} products with images!")

if __name__ == "__main__":
    seed_v3()
