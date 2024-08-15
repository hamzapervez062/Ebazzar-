#function based middleware
from django.http import HttpResponse
from .models import Product, Category, Review
from django.shortcuts import render, redirect
from django.urls import resolve

# def my_middleware(get_response):
#     #one time configuration and initialization  
#     print("One time initialization")
#     def my_function(request):
#         print("This is before view")
#         response = get_response(request)
#         request.session['p'] = Product.objects.get()
#         print("This is after view")
#         return response 
#     return my_function

class AnotherMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        #one time configuration and initialization
        print("One time initialization")
    def __call__(self, request):
        #code to be executed for each request before the view (and later middleware) are called
        print("This is before views")
        response = self.get_response(request)
        resolver_match = resolve(request.path)
        # print(resolver_match)
        
        if resolver_match.view_name == 'productdetail':  # Ensure this matches your view name
            item_id = resolver_match.kwargs['slug']  # Assuming 'slug' contains the product ID
            product_id = Product.objects.get(slug=item_id).id
            # Get existing clicked item IDs from session
            clicked_ids = request.session.get('clicked_item_ids', []) 
            if product_id not in clicked_ids:
                # Append new ID
                clicked_ids.insert(0, product_id)
                # Save updated list back to session
                request.session['clicked_item_ids'] = clicked_ids  
            elif product_id in clicked_ids:
                #update the list index 
                clicked_ids.remove(product_id)
                # clicked_ids.insert(0, product_id)
                request.session['clicked_item_ids'] = clicked_ids

            print(clicked_ids)
        return response