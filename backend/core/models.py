from django.db import models

# Create your models here.


class UselessModel(models.Model):
    name = models.CharField(max_length=255)
