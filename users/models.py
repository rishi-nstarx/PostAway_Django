from django.db import models
from django.core.exceptions import ValidationError

import re

# Create your models here.
def validate_username(value):
    if not re.match(r'^[A-Za-z0-9]+$', value):
        raise Exception("User must contain only numbers and charaters", params={"value":value},)


class Users(models.Model):
    
    username = models.CharField(max_length=20, unique=True, validators=[validate_username])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='photos/', blank=True, null=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"