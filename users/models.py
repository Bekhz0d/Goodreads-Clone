from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    picture = models.ImageField(default='anonim_user.png', upload_to='profile_pictures/')
