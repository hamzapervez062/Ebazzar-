from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.http import HttpResponseRedirect 
from django.contrib.auth.models import User # this is the default user model in django
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages   
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from Products.models import Category, Product
from Order.models import Order_item, Paymentinfo, Shippinginfo
from .forms import ProfileForm
from .models import Profile, CustomUser


# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
#login decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

def sign_up(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # fm = UserCreationForm(request.POST)
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            first_name = fm.cleaned_data['first_name']
            last_name = fm.cleaned_data['last_name']
            phone_number = fm.cleaned_data['phone_number']
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password1']
            user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email,  password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('Account/activate.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/login/?command=verification&email='+email)
    else:
        # fm = UserCreationForm()
        fm = SignUpForm()
        
    return render(request, 'Account/register.html', {'form':fm, 'categories': categories})

#login page
def log_in(request):
    if not request.user.is_authenticated:
        categories = Category.objects.all()	
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                request.session['user'] = email
                print('outside', request.session.get('user'))
                messages.success(request, 'Logged in Successfully')
                return HttpResponseRedirect('/login/')
            else:
                messages.success(request, 'Invalid Username or Password')
                return HttpResponseRedirect('/login/')
        return render(request, 'Account/signin.html', {'categories': categories})
    
    else:
        return HttpResponseRedirect('/dashboard/')
    
# send email with verification link
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('signup')

def dashboard(request):
    if request.user.is_authenticated:
        ord = Order_item.objects.filter(user=request.user).all().order_by('-created_at')
        dup_r = [] # to remove duplicate order numbers
        for o in ord:
            if o.order_number not in dup_r:
                dup_r.append(o.order_number)

        orde = [] # to store all orders with same order number 
        for k in dup_r:  
            order = Order_item.objects.filter(order_number=k)
            orde.append(order)
        user = request.user
        return render(request , 'Account/dashboard.html', {'order':orde, 'user':user})
    else:
        return HttpResponseRedirect('/login/')
    

def profile(request):
   if request.user.is_authenticated:
        user = request.user
        profile_pic = Profile.objects.get(user__id = request.user.id).image.url
        if request.method == 'POST':
                current_user = Profile.objects.get(user__id = request.user.id)
                
                edit_user = User.objects.get(id = request.user.id)
                full_name = request.POST.get('full_name')
                name_parts = full_name.split(' ')
                first_name = name_parts[0] 
                last_name = name_parts[-1]
                edit_user.first_name = first_name
                edit_user.last_name = last_name
                edit_user.phone_number = request.POST.get('phone_number')
                
                fm = ProfileForm(request.POST or None, request.FILES or None, instance = current_user)
                if fm.is_valid():
                    edit_user.save()
                    fm.save()
                    messages.success(request, 'Profile Updated Successfully')
                    return HttpResponseRedirect('/profile/')
        else:
            initial_dict = { 
            'full_name': request.user.first_name + " " + request.user.last_name,
            'phone_number': request.user.phone_number,
        }
            profile = Profile.objects.get(user__id = request.user.id)
            fm = ProfileForm(instance = profile,  initial = initial_dict)

        return render(request, 'Account/profile.html', {'user':user, 'form':fm, 'profile_pic':profile_pic})
   else:
       return HttpResponseRedirect('/login/')
    
    
# logout page
@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully')
    return redirect('/login/')


