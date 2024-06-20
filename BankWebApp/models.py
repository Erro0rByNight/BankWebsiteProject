from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.datetime.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    account_number = models.CharField(max_length=20, unique=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='customer_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_set', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Transfer(models.Model):
    sender = models.ForeignKey(Customer, related_name='sent_transfers',on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, related_name='received_transfers', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer from {self.sender} to {self.receiver} of {self.amount} on {self.timestamp}"