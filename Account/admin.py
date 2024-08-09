from django.contrib import admin
from django.contrib.auth.models import User # this is the default user model in django
from django.contrib.auth import get_user_model
from .models import Profile
User = get_user_model()

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

  

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'phone_number', 'bio', 'gender', 'verified']


#mix profile info and user
class ProfileInline(admin.StackedInline):
    model = Profile
#Extend User Model 
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = [ 'email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_active']
    field =  ['email', 'first_name', 'last_name', 'phone_number', 'is_admin',]
    inlines = [ProfileInline]
#Unregister the old way
admin.site.unregister(User)

#Re-Register the new way
admin.site.register(User, UserAdmin)

