import string
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):

    phone_number_validator = RegexValidator(
        regex=r'^\d{1,15}$',  # This regex allows 1 to 15 digits
        message='Phone number must contain only digits.',
        code='invalid_phone_number'
    )

    password_validator = RegexValidator(
        regex=r'^(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        message='Password must contain at least one number and one special character. It should be at least 8 characters long.',
        code='invalid_password'
    )

    # Override the AbstractBaseUser's password field to include the validators
    


    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,null=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[phone_number_validator]
    )
    password = models.CharField(validators=[MinLengthValidator(8), MaxLengthValidator(128), password_validator], max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    referrer = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='referred_users')
    referral_code = models.CharField(max_length=10,unique=True,blank=True,null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','phone_number']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
    
    def generate_referral_code(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(10))
    
    def save(self,*args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

# Add related_name to avoid clashes with auth.User
CustomUser._meta.get_field('groups').remote_field.related_name = 'customuser_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_permissions'



class userAddress(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    addressType = models.CharField(max_length=10)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    address = models.CharField(max_length=50,null=False)
    street = models.CharField(max_length=50,null=False)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state= models.CharField(max_length=50,null=False)
    pincode = models.CharField(max_length=10,null=False)

    def __str__(self) -> str:
        return self.user.first_name
    