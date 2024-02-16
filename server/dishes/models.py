from django.db import models

# Create your models here.
class IngredientsModel(models.Model):
    reference = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.reference
    

class MenuItemsModel(models.Model):
    reference = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    item_ingredients = models.ManyToManyField(
        IngredientsModel, blank=True, default=None, related_name='item_ingredients')
    cover_image = models.ImageField(
        null=True, blank=True, upload_to='static/images')
    sale_status = models.CharField(max_length=200, null=True, blank=True)
    sale_price = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    popular_status = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.reference