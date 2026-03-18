from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True) # For UI enrichment

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    GENDER_CHOICES = [
        ('Women', 'Women'),
        ('Men', 'Men'),
        ('Unisex', 'Unisex'),
    ]
    SKIN_TYPE_CHOICES = [
        ('All', 'All Skin Types'),
        ('Oily', 'Oily'),
        ('Dry', 'Dry'),
        ('Combination', 'Combination'),
        ('Sensitive', 'Sensitive'),
    ]
    name = models.CharField(max_length=255)
    brand_ref = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    category_ref = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    
    # Legacy fields (keeping for compatibility during migration, will move to properties)
    brand = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=100, blank=True)
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    discount = models.IntegerField(default=0) 
    rating = models.FloatField(default=0.0)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_external_url = models.URLField(max_length=500, blank=True, null=True)
    stock = models.IntegerField(default=0)
    shade = models.CharField(max_length=100, blank=True, null=True)
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES, default='All')
    
    # Homepage Section Flags
    is_trending = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand_name} - {self.name}"

    @property
    def brand_name(self):
        return self.brand_ref.name if self.brand_ref else self.brand

    @property
    def category_name(self):
        return self.category_ref.name if self.category_ref else self.category

    @property
    def image_url(self):
        # 1. Prioritize external URLs (already full links like Unsplash)
        if self.image_external_url and (self.image_external_url.startswith('http') or 'images.unsplash.com' in self.image_external_url):
            return self.image_external_url
            
        # 2. Use local file url if it's there and not just a dummy string
        if self.image and hasattr(self.image, 'url'):
            if not self.image.name.endswith('placeholder.jpg'): # and self.image.name != "":
                return self.image.url
        
        # 3. Dynamic Unsplash Fallback Map (Guarantees elegant high-quality images)
        cat_name = self.category_name.strip() if self.category_name else ""
        # 3. Dynamic Unsplash Fallback Map
        cat_name = (self.category_name or self.category or "").strip().lower()
        
        mapping = {
            'lipstick': 'photo-1586776101345-0e6d6232537c',
            'foundation': 'photo-1596704017254-9b121068fb31',
            'blush': 'photo-1522335789203-aabd1fc54bc9',
            'skincare': 'photo-1556228578-0d85b1a4d571',
            'men': 'photo-1552046122-03184de8560c',
        }
        
        photo_id = mapping.get(cat_name, 'photo-1620916566398-39f1143ab7be')
        
        # Ensure we always return a valid string
        return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&q=80&w=800"

    @property
    def discounted_price(self):
        return self.price * (100 - self.discount) / 100
