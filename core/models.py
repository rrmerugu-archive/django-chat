from django.db import models
 

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, password=None):
        if not username:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            first_name=first_name,
            is_staff=False,
            is_active=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, password):
        user = self.create_user(username= username,
                first_name=first_name,
                password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def register_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError("Users must have an email address")
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)

        ## gather the token for the user and return it
        return user




class User(AbstractBaseUser):
    
    user_id = models.AutoField(primary_key=True)
    username =  models.CharField(max_length=30, blank=True, null=True)
    email    =  models.EmailField(max_length=150, blank=False, primary_key=False,  unique=True)
    date_joined =  models.DateTimeField(auto_now_add=True, null=True)
    first_name = models.CharField(max_length=10, blank=True)
    last_name = models.CharField(max_length=10, blank=True, null=True)
    profile_pic = models.FileField(upload_to='user-profile-pic', default="http://jnrgym.com/wp-content/uploads/2013/08/Facebook-no-profile-picture-icon-620x389.jpg")

    # Permission | Administration Purpose
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)   
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name',]

    
    objects = CustomUserManager()






    def __str__(self): # __unicode__ on Python 2
        return self.email
    # These are needed for the admin
    # https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#custom-users-and-django-contrib-admin
    # Full example - https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#a-full-example

    def get_full_name(self):

        return "%s %s"%(self.first_name, self.last_name or '')

    def get_short_name(self):
        return "%s" %self.first_name


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        app_label = "core"

 



    
    def get_basic_info(self):
        data = {}
        data['username']  = self.username
        data['user_id'] = self.user_id
#         data['profile_pic'] = self.profile_pic
        return data

class Comments(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=1000)