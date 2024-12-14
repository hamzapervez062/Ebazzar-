#function based middleware
from django.http import HttpResponse
from .models import Product, Category, Review
from django.shortcuts import render, redirect
from django.urls import resolve
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.deprecation import MiddlewareMixin


# class CustomSessionMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Check if the session already exists
#         if not request.session.session_key:
#             # Create a new session if it doesn't exist
#             request.session.create()

#         # This ensures we have a session_key available
#         print(request.session.session_key)  # Debug output




# class AnotherMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response
#         #one time configuration and initialization
#         print("One time initialization")
#     def __call__(self, request):
#         #code to be executed for each request before the view (and later middleware) are called
#         print("This is before views")
#         response = self.get_response(request)
#         resolver_match = resolve(request.path)
#         # print(resolver_match)
        
#         if resolver_match.view_name == 'productdetail':  # Ensure this matches your view name
#             item_id = resolver_match.kwargs['slug']  # Assuming 'slug' contains the product ID
#             product_id = Product.objects.get(slug=item_id).id
#             # Get existing clicked item IDs from session
#             clicked_ids = request.session.get('clicked_item_ids', []) 
#             if product_id not in clicked_ids:
#                 # Append new ID
#                 clicked_ids.append(product_id)
#                 # Save updated list back to session
#                 request.session['clicked_item_ids'] = clicked_ids  
#             print(clicked_ids)
#         return response

class AnotherMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization
        print("One time initialization")
    
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called
        print("This is before views")
        response = self.get_response(request)
        resolver_match = resolve(request.path)
        
        if resolver_match.view_name == 'productdetail':  # Ensure this matches your view name
            item_id = resolver_match.kwargs['slug']  # Assuming 'slug' contains the product ID
            product_id = Product.objects.get(slug=item_id).id
            
            # Get existing clicked item IDs from session
            clicked_ids = request.session.get('clicked_item_ids', [])
            print(clicked_ids,"old")
            
            if product_id in clicked_ids:
                # Move the existing item to the front
                clicked_ids.remove(product_id)
            else:
                # If not already in the list, just append it
                clicked_ids.append(product_id)
            
            # Add the product_id to the front of the list
            clicked_ids.insert(0, product_id)
            
            # Limit the list size if necessary (e.g., to the last 4 items)
            clicked_ids = clicked_ids[:4]
            
            # Save updated list back to session
            request.session['clicked_item_ids'] = clicked_ids  
            print(clicked_ids,"new")

        return response