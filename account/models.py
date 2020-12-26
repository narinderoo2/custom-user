from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

class UserManger(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("User should have a not none")
        elif email is None:
            raise TypeError("email should have a not none")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using= self.db)
        return user

    def create_superuser(self,username,email,password=None):
        if password is None:
            raise TypeError("Password must be correct")

        user = self.create_user(username,email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=250,unique=True)
    password = models.CharField(max_length=120)
    phone = models.IntegerField(null=True,blank=True)
    Location = models.CharField(max_length=200,null=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    cerate_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']

    objects = UserManger()

    def __str__(self):
        return self.email

    def tokens(self):
        return ''




# token genrate for every register user
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    


# second post model
""" This post model add with user
        means:- only auth user create a post in self account
        but use ForgienKey time not add Use
e:g user = models.ForeginKey(User,on_delete=models.CASCADE)  #it is create a problem 
e:g user = models.ForeginKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) #this is correct """

class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    body = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title