from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Cart
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from Products.models import Product
from django.contrib import messages
#login decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required(login_url='login')
def AddToCart(request, id):
  if request.user.is_authenticated:
    product = Product.objects.get(id=id)
    if request.method == 'POST':
      color = request.POST.get('radio_color')
      size = request.POST.get('radio_size')
      print("color: ", color)
      print("size: ", size)
      print()

      cart_items = Cart.objects.filter(products=product, user=request.user, color=color, size=size)
      if cart_items.exists():
        cart = cart_items.first() # it will return the first object from the queryset like cart_items[0]
        # cart = Cart.objects.get(products=product, user=request.user, color=color, size=size)
        cart.quantity += 1
        # product.quantity -= 1
        # product.save()
        cart.save()
        print('cart updated')

      else:
        cart = Cart.objects.create(
          products=product,
          user=request.user,
          quantity=1,
          color=color,
          size=size
        )
        print()

        # product.quantity -= 1
        # product.save()  
        print('cart created')
      return redirect('/cart/')
  else:

    return redirect('/login/')
       

    # try:
    #   cart = Cart.objects.get(products=product, user=request.user, color=color, size=size)
    #   cart.quantity += 1
    #   cart.color = color
    #   cart.size = size
    #   product.quantity -= 1
    #   product.save()
    #   cart.save()
    #   print('cart updated')

    # except Cart.DoesNotExist:
    #   cart = Cart.objects.create(
    #     products=product, 
    #     user=request.user,
    #     quantity=1,
    #     color=color,
    #     size=size
    #   )
    #   product.quantity -= 1
    #   product.save()
    #   print('cart created')
    # return redirect('/cart/')
      
# @login_required(login_url='login')
def CartView(request):
    if request.user.is_authenticated:
      #fetch cart based on user
      cart = Cart.objects.filter(user=request.user).order_by('-date_added')
      #get cart count
      cart_count = cart.count
      for item in cart:
         request.session['cart_id'] = item.cart_id
         print(request.session.get('cart_id'))
      #get total
      total = 0
      for item in cart:
          total += item.sub_total()
      # 2% tax on total amount and save in tax variable
      tax = round(float(total) *  0.02, 2)
      grand_total = round(tax + float(total), 2)

      return render(request, 'Cart/cart.html', {'cart': cart, 'cart_count': cart_count, 'total': total, 'tax': tax, 'grand_total': grand_total})
    else:
       cart = None
       return render(request, 'Cart/cart.html', {'cart': cart})

def DeleteCart(request, id):
    #---------------------------------------------------------------------------
    # product_id = Cart.objects.get(cart_id=id).products.id
    # print(product_id)
    # product = Product.objects.get(id=product_id)
    #---------------------------------------------------------------------------

    cartQuantity = Cart.objects.get(cart_id=id).quantity

    if request.user.is_authenticated:
            try:
                # Get the cart item, ensuring it belongs to the current user
                cart = Cart.objects.get(cart_id=id, user=request.user)
                
                # Increase the product quantity by the cart quantity
                # product.quantity = product.quantity + cartQuantity
                # product.save()

                # Delete the cart item
                cart.delete()
                print('cart deleted')
            except Cart.DoesNotExist:
                print('cart does not exist')
                messages.error(request, 'Cart item does not exist')
                
    else:
        messages.warning(request, 'You must be logged in to delete cart items.')

    return redirect('/cart/')

#update cart
def UpdateCart(request, id):
    #---------------------------------------------------------------------------
    # product_id = Cart.objects.get(cart_id=id).products.id
    # print(product_id)
    # product = Product.objects.get(id=product_id)
    #---------------------------------------------------------------------------
    cart = Cart.objects.get(cart_id=id, user=request.user)
    if cart:
      if request.method == 'POST':
          quantity = request.POST.get('quantity')
          quantity = int(quantity)


          if quantity > cart.products.quantity:
              messages.warning(request, 'you can not add more than available stock')
              
          elif quantity == cart.quantity:
              messages.warning(request, 'Item quantity is same as before')
          
          elif quantity < 1:
              messages.warning(request, 'cart quantity must be greater than 0')
          else:	
              # product.quantity = product.quantity  - quantity
              # product.save()

              cart.quantity = quantity
              cart.save()
      else:
          return render(request, 'Cart/cart.html')	
    else:
      return render(request, 'Cart/cart.html', {'error': 'Product does not exist in cart'})
    return redirect('/cart/')

#quantity increment 
def QuantityUp(request, id):
    #get product id from cart model , it is use for the quntity update when increment
    #---------------------------------------------------------------------------
    # product_id = Cart.objects.get(cart_id=id).products.id
    # print(product_id)
    # product = Product.objects.get(id=product_id)
    #---------------------------------------------------------------------------

    cart = get_object_or_404(Cart, cart_id=id, user=request.user)
    
    if cart.quantity >= cart.products.quantity:
      messages.warning(request, 'you can not add more than available stock')
    
    elif cart.products.quantity !=0:
      cart.quantity += 1
      cart.save()

      # product.quantity -= 1
      # product.save()

    return redirect('/cart/')

#quantity decrement
def QuantityDown(request, id):
    #get product id from cart model  , it use for the quntity update when decrement
    #---------------------------------------------------------------------------
    # product_id = Cart.objects.get(cart_id=id).products.id
    # print(product_id)
    # product = Product.objects.get(id=product_id)
    #---------------------------------------------------------------------------

    # it will get the cart object with the given id and user
    cart = get_object_or_404(Cart, cart_id=id, user=request.user)
    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()

        # product.quantity += 1
        # product.save()
    else:
        messages.warning(request, 'cart quantity must be greater than 0')

    return redirect('/cart/')
      