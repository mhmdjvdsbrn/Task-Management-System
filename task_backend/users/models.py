import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.core.validators import MaxValueValidator, MinValueValidator
from task_backend.users.validators import validate_phone_number
from task_backend.users.hasher import SHA256PasswordHasher

# Manager for creating users and superusers
class BaseUserManager(BUM):
    def create_user(self, phone, is_active=True, is_admin=False, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(phone=phone, is_active=is_active, is_admin=is_admin)

        if password is not None:
            hashed_password = SHA256PasswordHasher().encode(password, salt=None)
            user.password = hashed_password
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(phone=phone, is_active=True, is_admin=True, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class BaseUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(validators=[validate_phone_number], max_length=13, unique=True)
    email = models.EmailField(verbose_name="email address", unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True)

    objects = BaseUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def is_staff(self):
        return self.is_admin


def get_profile_avatar_path(instance, filename):
    folder_name = f"{instance.first_name}_{instance.last_name}"
    return os.path.join('images/profiles', folder_name, filename)

class Profile(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to=get_profile_avatar_path, default='images/profiles/avatar.jpg') 
