from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(
        max_length=155,
        verbose_name="номер телефона",
        null=True, blank=True
    )

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователи"