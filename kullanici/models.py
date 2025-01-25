from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class KullaniciManager(BaseUserManager):
    def create_user(self, identity_no, email, password=None, **extra_fields):

        if not identity_no:
            raise ValueError('The Identity No field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(identity_no=identity_no, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identity_no, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(identity_no, email, password, **extra_fields)
class Kullanici(AbstractUser):
    username = None
    identity_no = models.CharField(max_length=11, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    phone_number = models.CharField(max_length=11, null=False, unique=True)
    address = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'identity_no'
    REQUIRED_FIELDS = ['email']

    objects = KullaniciManager()
    def __str__(self):
        return f"{self.identity_no}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


