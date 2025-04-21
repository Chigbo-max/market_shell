from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

class User(AbstractUser):
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user/profile/image", null=True, blank=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])])
