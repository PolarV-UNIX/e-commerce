from django.contrib.auth.models import (
    BaseUserManager, 
    PermissionsMixin, 
    AbstractBaseUser
)
from django.db import models
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta


""" USER'S OBJECT MANAGER """
class UserManager(BaseUserManager):
    def create_user(self, phone=None, first_name=None, last_name=None, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(
            phone=phone, 
            first_name=first_name,
            last_name=last_name, 
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone=None, first_name=None, last_name=None, password=None, **extra_fields):
        # extra_fields.setdefault('type', 'admin')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(phone, first_name, last_name, password, **extra_fields)

""" USER MODEL """
class User(AbstractBaseUser, PermissionsMixin):
    # USER'S TYPE
    USER_TYPE = (
        (1, 'Seller'),
        (2, 'Customer')
    )
    type_user = models.PositiveSmallIntegerField(choices=USER_TYPE, default=2)
    device_user = models.ForeignKey('User.UserDevice', on_delete=models.SET_NULL, null=True, blank=True)
    # VERIFICATION CODE
    """ store the codes here to authentication code """
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires_at = models.DateTimeField(null=True, blank=True)
    
    # EXPIRATION DATE
    expiration_date = models.DateTimeField(null=True, blank=True)
    
    # USER'S FULL-NAME
    first_name = models.CharField(max_length=50, null=True,blank=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    
    # USER'S PHONE-NUMBER 
    phone_regex = RegexValidator(
        regex = r'^09\d{9}$',
        message = "Phone number is invalid"
    )
    phone = models.CharField(max_length=11, validators=[phone_regex], unique=True)
    
    # USER'S EMAIL
    email = models.EmailField(max_length=254, null=True, blank=True)
    
    # USER'S DATE
    date_joined = models.DateTimeField(auto_now_add=True)
    modifiy_date = models.DateTimeField(auto_now=True)
    
    # USER'S AVATAR
    avatar = models.ImageField(blank=True, null=True, upload_to="media/profile_photos/")
    
    # USER'S BIRTHDAY
    birth_day = models.DateField(null=True, blank=True) 
    
    # USER'S GENDER
    GENDER = (
        (True, "male"),
        (False, "female")
    )
    gender = models.BooleanField(default=True) 
    
    # USER'S SITUATION
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # USER'S FAVORITE
    favorits = models.ManyToManyField('Product.Product', related_name='favorited_by', blank=True)
    
    # USER'S MANAGER
    objects = UserManager()
    
    # USER'S REQUEIREMENTS FOR REGISTER
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # CODE GENERATOR
    def generateVerificationCode(self):
        code = get_random_string(length=6, allowed_chars='0123456789')
        self.verification_code = code
        # Set the expiration timestamp 2 minutes from now
        self.code_expires_at = timezone.now() + timedelta(minutes=2)
        # Set the expiration date for registeration
        self.Expiration_date = timezone.now() + timedelta(days=60)
        self.save()
        
    # METADATA
    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['phone']
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return f"{self.first_name}"
    
    def __str__(self):
        return self.first_name
    
    
""" USER'S DEVICE MODEL """    
class UserDevice(models.Model):
    # USER'S DEVICE TYPE
    DEVICE_PLATFORM = (
        (1, "web"),
        (2, "ios"),
        (3, "android")
    )
    device = models.PositiveSmallIntegerField(
        choices=DEVICE_PLATFORM, 
        default=1,
        null=True,
        blank=True
        )
    
    # IP 
    ip_address = models.GenericIPAddressField(protocol="both", unpack_ipv4=True)
    
    # USER'S FIELD
    user_id = models.ForeignKey("User.User", on_delete=models.CASCADE)
    
    # UUID OF USER'S DEVICE
    device_uuid = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True )
    modified_at = models.DateTimeField(auto_now=True)
    
    # METADATA
    class Meta:
        db_table = "user's-devices"
        
    def __str__(self):
        return {self.device}
