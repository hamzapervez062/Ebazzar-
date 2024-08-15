from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Avg
from Account.models import Profile
# Create your models here.
# Category model
class Category(models.Model):
    CATEGORY_CHOICES = (
    ('TShirt', 'TShirt'),
    ('Jeans', 'Jeans'),
    ('Jacket', 'Jacket'),
    ('Sweater', 'Sweater'),
    ('Shorts', 'Shorts'),
    ('Socks', 'Socks'),
    ('Shoes', 'Shoes'),
    ('Parse', 'Parse'),
    ('Heals', 'Heals'),


)
    title = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        # return reverse("storeview", args=[self.slug])
        return f'/store/category/{self.slug}/'

    def __str__(self):
        return self.title
    
    

# Product model
class Product(models.Model):
    Product_Status = (
    ('In Stock', 'In Stock'),
    ('Out of Stock', 'Out of Stock'),
    ('Coming Soon', 'Coming Soon'),
    )

    Product_Size = (
        ('S', 'S'),
        ('Medium', 'Medium'),
        ('L', 'L'),
        ('XL', 'XL'),
    )

    Product_Color = (
        ('Black', 'Black'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Grey', 'Grey'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relationship
    image = models.ImageField(upload_to='products')
    discount = models.DecimalField(max_digits=10, decimal_places=0, default=0)  
    # slug = models.SlugField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True) # AutoSlugField is used to create unique slug for each product
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    quantity = models.IntegerField(default=10) #in stock available qunatity
    product_status = models.CharField(max_length=255, choices=Product_Status, default='In Stock')
    size = models.CharField(max_length=255, choices=Product_Size, null=True, blank=True)
    color = models.CharField(max_length=255, choices=Product_Color, null=True, blank=True)


    def get_absolute_url(self):
        return f'/store/category/{self.category.slug}/{self.slug}/'
    
    # def get_url(self):
    #     return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.title
    
rating_choices = (
    (1, '1'),	
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)
    
class Review(models.Model):
    review_title = models.CharField(max_length=255)
    review_description = models.TextField(max_length=255)
    review_rating = models.FloatField(choices=rating_choices)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True) #for profile pic
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def product_slug(self):
        return self.product.slug
    
    def product_avg_rating(self):
        return Review.objects.filter(product=self.product).aggregate(Avg('review_rating', default=0))['review_rating__avg']


    
