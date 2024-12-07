from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('dietitian', 'Dietitian'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    diet_plan = models.ForeignKey('diet_plan.DietPlan', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'role']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_admin(self):
        return self.role == 'admin'

    def clean(self):
        if self.role not in dict(self.ROLE_CHOICES):
            raise ValidationError("Invalid role")

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, app_label):
        return self.is_active

    def save(self, *args, **kwargs):
        if not self.is_staff:
            self.is_staff = self.role == 'admin'
        if not self.is_superuser:
            self.is_superuser = self.role == 'admin'
        super().save(*args, **kwargs)


class DietitianClient(models.Model):
    dietitian = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clients',
        limit_choices_to={'role': 'dietitian'},
        null=True,
        blank=True
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dietitians',
        limit_choices_to={'role': 'client'}
    )

    class Meta:
        unique_together = ('dietitian', 'client')
