
from django.db.models.base import Model as Model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Cart.models import Cart
from .models import Product, Category, Review
from django.views.generic import ListView, DetailView
from Account.models import Profile

# Create your views here.

#it for index page to show all list of items
class homeListView(ListView):
    model = Product
    template_name = 'Products/index.html'
    context_object_name = 'products'

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_superuser:
    #         return redirect('/admin/')
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all().order_by('-created_at')[:8] # it will show the latest 6 products

        #review count
        for product in context['products']:
            product.review_count = Review.objects.filter(product=product).count()

        #max rating
        max_rating = 5
        context['max_rating'] = range(max_rating) 
        for product in context['products']:
            product_reviews = Review.objects.filter(product=product)  
            product.average_rating = product_reviews.aggregate(Avg('review_rating', default=0))['review_rating__avg']
            print(product.average_rating)
        return context
    
   

#it is for store page

# def Store(request):
#     products = Product.objects.all()
#     products_count = products.count()
#     categories = Category.objects.all()
#     context = {
#         'products': products,
#         'categories': categories,
#         'products_count': products_count,
#     }
#     return render(request, 'Products/store.html', context)

class Store(ListView):
    model = Product
    template_name = 'Products/store.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')
    
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products_count'] = Product.objects.all().count() # it will count total Items found
        return context

    
# class storeRedirectView(RedirectView):
#     pattern_name = "storeview"

#     def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
#         return super().get_redirect_url(*args, **kwargs)


#it is for store page to show items based on cartegory.
class storeListView(ListView):
    model = Product
    template_name = 'Products/store.html'
    context_object_name = 'products'
    paginate_by = 6

    # 
    def get_queryset(self):  
        return Product.objects.filter(category__slug=self.kwargs['post']).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products_count'] = self.get_queryset().count() # it will count total Items found
        return context
    

#Search 
def SearchItem(request):
    query = request.GET['keyword']
    products = Product.objects.filter(title__icontains=query)
    products_count = products.count()
    print(query)	
    context = {
        'products': products,
        'products_count': products_count, # it will Items found
    } 
    return render(request, 'Products/store.html', context)

#Price Range
def PriceRange(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price and max_price:
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        products = Product.objects.filter(price__gte=min_price)
    elif max_price:
        products = Product.objects.filter(price__lte=max_price)
    else:
        products = Product.objects.all()

        
    products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'Products/store.html', context)

from django.db.models import Avg

#Detail of each Product
class ProductDetails(DetailView):
    model = Product
    template_name = 'Products/product_detail.html'
    context_object_name = 'products'
    slug_url_kwarg = 'slug'
   
    # fm = CartForm()  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(slug=self.kwargs['slug'])
        context['cart_count'] = Cart.objects.all().count()
        context['reviewfetch'] = Review.objects.filter(product__slug=self.kwargs['slug'])
        context['review_count'] = Review.objects.filter(product__slug=self.kwargs['slug']).count()

        #average rating
        review_avg = round(Review.objects.filter(product__slug=self.kwargs['slug']).aggregate(Avg('review_rating', default=0))['review_rating__avg'],1)
        context['review_avg'] = review_avg	
        #max rating
        average_rat = int(review_avg)
        context['average_rat'] = average_rat
        max_rating = 5
        context['max_rating'] = range(max_rating)      
        return context
    
def ReviewSubmit(request, post, slug):
    product =  Product.objects.get(slug=slug)
    if request.method == 'POST':
        review_rating = request.POST.get('rating_stars')
        review = request.POST.get('review')
        review_title = request.POST.get('subject')
        user = request.user
        if Review.objects.filter(product=product, user=user).exists():
           return HttpResponse("Review with this User already exists.")
        
        if not Review.objects.filter(product=product, user=user).exists():
            print(review_rating, review, review_title, user, product)
            review = Review.objects.create(product=product, user=user, review_rating=review_rating, review_description=review, review_title=review_title, 
                profile=request.user.profile)
            review.save()
    
    return redirect(f'/store/category/{post}/{slug}/')

def deleteReview(request, post, slug):
    product =  Product.objects.get(slug=slug)
    if request.method == 'POST':
        review = Review.objects.get(product=product, user=request.user)
        review.delete() 

    return redirect(f'/store/category/{post}/{slug}/')





    


