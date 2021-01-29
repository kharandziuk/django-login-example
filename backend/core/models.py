from django.db import models
from django.contrib.auth import get_user_model

from django.conf import settings

# Create your models here.
UserModel = get_user_model()


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items"
    )
