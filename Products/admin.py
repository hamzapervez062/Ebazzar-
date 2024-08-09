from django.contrib import admin
from .models import Product, Category
from .models import Review



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'discount', 'slug', 'created_at', 'updated_at', 'quantity',]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'review_rating','profile', 'created_at', 'updated_at', 'review_description', 'product_slug']



