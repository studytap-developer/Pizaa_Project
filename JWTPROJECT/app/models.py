from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Custom  User manger here
class UserManager(BaseUserManager):
    def create_user(self,email,name,is_admin=False,password=None):
        """ create and save a user with the given email,name,and password"""
        if not email:
            raise ValueError("user Must have email")
        user=self.model(
            email=self.normalize_email(email),
            name=name,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,name,is_admin=True,password=None):
        """ create and save a Superuser with the given email,name,and password"""
       
        user=self.model(
            email=self.normalize_email(email),
            name=name,
            password=password,
            is_admin=is_admin
        )
        user.is_admin=True
        user.save(using=self._db)
        return user

# Custom  User models here.
class User(AbstractBaseUser):
    email=models.EmailField(verbose_name="Email",max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["name","is_admin"]

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.name

    def has_perm(self,perm,obj=None):
        "Does the user have a specific permison"
        # simple ans: yes /no
        return self.is_admin
    
    def has_module_perms(self,app_label):
        "does the user  have permission to view the app app_leabel?"
        # simple ans: yes /no
        
        return True

    @property
    def is_staff(self):
        "IS user a memeber of staff"
        # simple possible ans:All admin are staff
        return self.is_admin



