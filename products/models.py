from django.db import models


class Product(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now=True)