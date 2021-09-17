from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# Manager for Custom User Model
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email cannot be None")
        if not username:
            raise ValueError("Username cannot be None")
        
        user =  self.model(
                    email = self.normalize_email(email),
                    username = username,
                )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(email, username, password = password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom User Model
class User(AbstractBaseUser):
    # Basic fields required for a custom user model.
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=40, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Extra fields added as per your requirements.
    # first_name = models.CharField(max_length=35)
    # last_name = models.CharField(max_length=35)
    profile_img = models.ImageField(null=True)
    bio = models.CharField(max_length=150, null=True)
    
    # Using this value for logging 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.email}"

    # These 2 func are for user roles.
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class Task(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Item(models.Model):
    # id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.status}"
