import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'galuxe_project.settings')
django.setup()

from products.models import Product

# Extensive Data Structures
CATEGORIES = {
    'Women': {
        'Skin Care': ['Face Wash', 'Cleanser', 'Toner', 'Moisturizer', 'Sunscreen', 'Serum', 'Face Oil', 'Night Cream', 'Eye Cream', 'Lip Balm', 'Face Mask'],
        'Makeup': ['Foundation', 'Concealer', 'Compact Powder', 'Primer', 'Blush', 'Highlighter', 'Eyeshadow', 'Eyeliner', 'Kajal', 'Mascara', 'Lipstick', 'Lip Gloss'],
        'Hair Care': ['Shampoo', 'Conditioner', 'Hair Oil', 'Hair Serum', 'Hair Mask'],
        'Body Care': ['Body Lotion', 'Body Butter', 'Body Scrub', 'Body Wash'],
        'Fragrance': ['Perfume', 'Eau de Parfum', 'Body Mist'],
        'Nail Cosmetics': ['Nail Polish', 'Nail Remover'],
    },
    'Men': {
        'Skin Care': ['Face Wash', 'Moisturizer', 'Sunscreen', 'Face Scrub'],
        'Shaving and Grooming': ['Shaving Cream', 'Aftershave Lotion', 'Beard Oil', 'Beard Balm'],
        'Hair Care': ['Shampoo', 'Conditioner', 'Hair oil', 'Hair Gel', 'Hair Wax'],
        'Fragrance': ['Perfume', 'Cologne', 'Body Spray'],
    }
}

BRANDS = {
    'Women': ['MAC', 'Estée Lauder', 'Lakmé', 'Maybelline', 'L\'Oréal', 'Nykaa', 'Kama Ayurveda', 'The Body Shop', 'Forest Essentials', 'Huda Beauty'],
    'Men': ['Beardo', 'The Man Company', 'Ustraa', 'Philips', 'Gillette', 'Park Avenue', 'Old Spice', 'Nivea Men', 'Axe']
}

SHADES = {
    'Lipstick': ['Ruby Red', 'Wine Red', 'Cherry Red', 'Nude Pink', 'Rose Pink', 'Peach Pink', 'Coral Orange', 'Deep Plum', 'Brown Nude', 'Chocolate Brown'],
    'Foundation': ['Ivory', 'Porcelain', 'Beige', 'Sand', 'Honey', 'Caramel', 'Mocha', 'Deep Cocoa'],
    'Nail Polish': ['Crimson', 'Petal Pink', 'Midnight Black', 'Gold Shimmer', 'Lavender', 'Mint Green'],
    'Eyeshadow': ['Nude Palette', 'Smokey Palette', 'Pink Palette', 'Golden Shimmer Palette']
}

IMAGES = [
    "https://images.unsplash.com/photo-1522335789203-aabd1fc5371c?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1596462502278-27bfdc4033c8?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1591130901020-ef93616f9476?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1617897903246-7dc903673733?auto=format&fit=crop&q=80&w=800"
]

def seed_v2():
    print("Clearing existing products...")
    Product.objects.all().delete()
    
    products_to_create = []
    
    # Generate 200 products
    for i in range(200):
        gender = random.choice(['Women', 'Men'])
        cat_group = random.choice(list(CATEGORIES[gender].keys()))
        category = random.choice(CATEGORIES[gender][cat_group])
        brand = random.choice(BRANDS[gender])
        
        name = f"{brand} {category} {'Gold' if i%2==0 else 'Elite'}"
        price = random.randint(300, 5000)
        discount = random.choice([0, 10, 15, 20, 25, 40])
        rating = round(random.uniform(3.5, 5.0), 1)
        
        shade = None
        if category in SHADES:
            shade = random.choice(SHADES[category])
            name += f" - {shade}"
            
        skin_type = random.choice(['All', 'Oily', 'Dry', 'Combination', 'Sensitive'])
        
        description = f"Experience the luxury of {brand}. This premium {category} is designed to give you a {shade if shade else 'flawless'} finish and long-lasting results. Perfect for {skin_type} skin."
        
        product = Product(
            name=name,
            brand=brand,
            category=category,
            gender=gender,
            price=price,
            discount=discount,
            rating=rating,
            description=description,
            stock=random.randint(10, 100),
            shade=shade,
            skin_type=skin_type,
            is_trending=(i < 15),
            is_best_seller=(20 < i < 35),
            is_new_arrival=(40 < i < 55)
        )
        products_to_create.append(product)

    Product.objects.bulk_create(products_to_create)
    print(f"Successfully seeded {Product.objects.count()} products!")

if __name__ == "__main__":
    seed_v2()
