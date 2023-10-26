from datetime import timezone
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
# 
from .validators import strongPassword,is_tunisian_phone_number

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True,)
    password = models.CharField(max_length=128, validators=[strongPassword],blank=False,null=False)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'),('F', 'Female'),], blank=False, null=False)
    phone_number = models.CharField(max_length=8, blank=False,null=False,validators=[is_tunisian_phone_number],unique=True)

    first_name = models.CharField(max_length=30,blank=False)
    last_name = models.CharField(max_length=30,blank=False)

    REQUIRED_FIELDS = ['email','first_name', 'last_name', 'gender', 'phone_number']

    def __str__(self):
        return self.username
    
