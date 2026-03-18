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
        mapping = {
            'Lipstick': 'photo-1631214500115-598fc2cb882e',
            'Foundation': 'photo-1596704017254-9b121068fb31',
            'Mascara': 'photo-1512496015851-a90fb38ba796',
            'Eyeshadow': 'photo-1512496015851-a90fb38ba796',
            'Perfume': 'photo-1541643600914-78b084683601',
            'Shampoo': 'photo-1526947425960-945c6e72858f',
            'Moisturizer': 'photo-1556228720-195a672e8a03',
            'Face Wash': 'photo-1556228578-0d85b1a4d571',
            'Serum': 'photo-1620916566398-39f1143ab7be',
            'Men': 'photo-1621607512214-68297480165e',
            'Beard Oil': 'photo-1655394009794-df4f7cd8582a',
            'Shaving Cream': 'photo-1695048200681-c0333e837e2b',
            'Grooming Kit': 'photo-1590666270543-9cc2d5257f86',
        }
        
        photo_id = mapping.get(cat_name, 'photo-1620916566398-39f1143ab7be')
        return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&q=80&w=800"

    @property
    def discounted_price(self):
        return self.price * (100 - self.discount) / 100
