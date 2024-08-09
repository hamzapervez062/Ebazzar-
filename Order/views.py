from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Cart
from Products.models import Product
from django.contrib import messages
from Order.forms import BillingForm
from Order.models import Paymentinfo
from .models import Order_item
from .models import Shippinginfo
#login decorator
from django.contrib.auth.decorators import login_required


# Create your views here.

def product_calculation(request):
    cart = Cart.objects.filter(user=request.user).order_by('-date_added')
    cart_count = cart.count
    total = 0
    for item in cart:
        total += item.sub_total()
    tax = round(float(total) *  0.02, 2)
    grand_total = round(tax + float(total), 2)
    return cart , cart_count , total , tax , grand_total

@login_required(login_url='login')        
def checkout(request):      
    # cart check before checkout
    cart = Cart.objects.filter(user=request.user).order_by('-date_added')
    if not cart.exists():
        messages.warning(request, 'Cart is empty')
        return redirect('/cart/')
    else: 
        cart , cart_count , total , tax , grand_total = product_calculation(request)
    if request.method == 'POST':
            fm = BillingForm(request.POST)
            if fm.is_valid():  
                request.session['shipping'] = fm.cleaned_data.get('email')
                print('outside', request.session.get('shipping'))
                
                if not Shippinginfo.objects.filter(email = request.session.get('shipping')).exists():
                    fm.save()
                    print("added")
                else:
                    fm = BillingForm(request.POST, instance=Shippinginfo.objects.get(email = request.session.get('shipping')))
                    fm.save()
                    print("updated")
                
                return redirect('/placeorder/')
            else:
                fm = BillingForm()
    else:
            fm = BillingForm()
    return render(request, 'Order/checkout.html', {'form':fm,'cart': cart, 'cart_count': cart_count, 'total': total, 'tax': tax, 'grand_total': grand_total})	

@login_required(login_url='login') 
def placeorder(request):
    cart = Cart.objects.filter(user=request.user).order_by('-date_added')
    if not cart.exists():
        messages.warning(request, 'Cart is empty')
        return redirect('/cart/')
    else: 
        cart , cart_count , total , tax , grand_total = product_calculation(request)
        
    shipping_info = Shippinginfo.objects.get(email = request.session.get('shipping'))

    return render(request, 'Order/place-order.html', {'shipping_info': shipping_info , 'cart': cart, 'cart_count': cart_count, 'total': total, 'tax': tax, 'grand_total': grand_total})	

@login_required(login_url='login') 
def editshippinginfo(request):
    #get shipping info based on user email
    shipping_info = Shippinginfo.objects.get(email = request.session.get('shipping'))
    # dictionary for initial data with  
    # field names as keys 
    initial_dict = { 
        "first_name":shipping_info.first_name,
        "last_name":shipping_info.last_name,
        "phone":shipping_info.phone,
        "address_line_1":shipping_info.address_line_1,
        "country":shipping_info.country,
        "state":shipping_info.state,
        "city":shipping_info.city,
        "email":shipping_info.email
    }
    if request.method == 'POST':
            #update shipping info
            fm = BillingForm(request.POST, instance=shipping_info) 
            if fm.is_valid():  
                fm.save()
                request.session['shipping'] = fm.cleaned_data.get('email')
                print('outside', request.session.get('shipping'))
            return redirect('/placeorder/')
    else:
            fm = BillingForm(initial=initial_dict, instance=shipping_info)
            
    cart , cart_count , total , tax , grand_total = product_calculation(request)
    return render(request, 'Order/checkout.html', {'form':fm,'cart': cart, 'cart_count': cart_count, 'total': total, 'tax': tax, 'grand_total': grand_total})	


import datetime
import random

pro_id =[]
def order_processing(request):
    if request.user.is_authenticated:
        carts, cart_count , total , tax , grand_total = product_calculation(request)
        cart = Cart.objects.filter(user = request.user)
        # if Order_item.objects.filter(user = request.user, cart__in = cart, shipping__email = request.session.get('shipping')).exists():
        #      return HttpResponse("Already ordered")

        shipping = Shippinginfo.objects.get(email = request.session.get('shipping'))
        payment = Paymentinfo.objects.create(user = request.user , payment_method="Cash On Delivery",
                                              amount_paid = grand_total, status = "Completed",
                                                created_at = datetime.datetime.now())    
        objs = []
        order_num = []
        num = random.randint(10000000, 99999999)
        for item in cart: 
            p_id = item.products.id
            pro_id.append(p_id)
            obj = Order_item.objects.create(user = request.user, cart=item, shipping = shipping, payment=payment, 
                                            order_total = grand_total,order_number = num, tax = tax, sub_total = total,
                                            quantity=item.quantity, product_price=item.products.price, product_id = p_id,
                                            item = item.products, status_delivery = 'Accepted')
            order_num.append(obj.order_number)
            objs.append(obj)

            #decrease product quantity
            product_id = Cart.objects.get(cart_id=item.cart_id).products.id
            product = Product.objects.get(id=product_id)
            product.quantity -= item.quantity
            product.save()

        #cart delete
        cart.delete()
        print("deleted")

        return redirect(f'/ordercomplete/{order_num[0]}/{payment.payment_id}/')
    
def order_complete(request, id, slug):
    if request.user.is_authenticated:
        order = Order_item.objects.filter(order_number = id)

        dic = {} # to 
        for f in order:
            details = {}
            
            #-----------------for title fetch using on product_id(method 1)------------------------
            # x = Product.objects.filter(pk = f.product_id)   
            # for i in x:
            #     details["title"] = i.title
            #-------------------or second method------------------------

            details["title"] = f.item.title
            details["qunatity"] = f.quantity
            details["product_price"] = str(float(f.product_price)) + " USD"
            dic[f.id] = details

        print(dic)

        payment = Paymentinfo.objects.get(payment_id = slug)
        # p = Order_item()
        # sub = p.sub_ttotal
        shipping_detail = Shippinginfo.objects.get(email = request.session.get('shipping'))
        return render(request, 'Order/order_complete.html', {'order': order, 'payment':payment, 'shipping':shipping_detail, 'dic': dic})
    else:
        return redirect('login')
