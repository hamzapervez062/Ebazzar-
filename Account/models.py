from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_delete, pre_delete, post_save, pre_save
from django.dispatch import receiver



# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("Email shoudn't be empty")
        if not password:
            raise ValueError("Password shoudn't be empty")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
    



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)	

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "password"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default = 'profile_pics/default.jpeg' ,  null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True, max_length=15)
    gender = models.CharField(max_length=255, choices=gender, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
    
post_save.connect(create_user_profile, sender=CustomUser)









