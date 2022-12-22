from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40)
    icon = models.ImageField()


class Product(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now=True)
    category = models.ManyToManyField(Category)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()