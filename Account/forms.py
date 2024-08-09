from django.contrib.auth.models import User # This is the default User model that Django provides
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm # This is the default UserCreationForm that Django provides 
from django import forms   
from django.contrib.auth import authenticate
from django.core import validators 
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm  , PasswordChangeForm, UserChangeForm


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # This removes the colon from all labels

    password2 = None # it remove this field
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    # password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', validators=[validators.EmailValidator], widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password1']
        labels = {'email': 'Email', 'firstname': 'First Name'} 
        widgets = {'first_name':forms.TextInput(attrs={'placeholder':'First name', 'class':'form-control',}),
                   'last_name':forms.TextInput(attrs={'placeholder':'Last name', 'class':'form-control'}),
                   'phone_number':forms.TextInput(attrs={'placeholder':'Phone number', 'class':'form-control', 'type':'tel'}),
                #    'email':forms.EmailInput(attrs={'placeholder':'Enter email here', 'class':'form-control'}),
                #    'password1':forms.PasswordInput(attrs={'placeholder':'Enter password here', 'class':'form-control'}),
                   }
        # def __init__(self, *args, **kwargs):
        #     super(SignUpForm, self).__init__(*args, **kwargs)
        #     self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        #     self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        #     self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        #     self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        #     for field in self.fields:
        #         self.fields[field].widget.attrs['class'] = 'form-control'

# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(label='Email', validators=[validators.EmailValidator], widget=forms.EmailInput(attrs={'class':'form-control'}), required=True)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}))
#     class Meta:
#         model = User
#         fields = ['email', 'password']
#         labels = {'email': 'Email', 'password': 'Password'}

# AuthenticationForm provie username and password fields, not email and password.
#profile form#
class ProfileForm(UserChangeForm):
    password = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # This removes the colon from all labels

    class Meta:
        model = Profile
        fields = ['full_name','image', 'phone_number', 'bio', 'gender']
        labels = {'full_name': 'Full Name','image': 'Profile Picture', 'phone_number': 'Phone Number', 'bio': 'Bio', 'gender': 'Gender'}

        widgets = {'full_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter full name here', 'label':'Full Name'}),	
                   'image':forms.FileInput(attrs={'class':'form-control',}),
                   'phone_number':forms.TextInput(attrs={'placeholder':'Enter phone number here', 'class':'form-control' , 'type': 'tel'}),
                   'bio':forms.TextInput(attrs={'placeholder':'Enter bio here', 'class':'form-control'}),
                   'gender':forms.Select(attrs={'class':'form-control'}), }
        
        
        
     
       
        

    
    
    
        
