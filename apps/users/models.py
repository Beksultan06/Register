from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255, unique=True)  # для сканера

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователи"