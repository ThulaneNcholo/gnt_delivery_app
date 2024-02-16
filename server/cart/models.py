from django.db import models
from dishes.models import *
from client.models import CustomerModel

class ItemIngredientsModel(models.Model):
    orderNumber = models.CharField(max_length=200, null=True, blank=True)
    item = models.ForeignKey(IngredientsModel, null=True, on_delete=models.CASCADE,
                              blank=True, default=None, related_name='item')
    status = models.CharField(max_length=200, null=True, blank=True, default = 'on')

    def __str__(self):
        return self.orderNumber


class CartItemsModel(models.Model):
    orderNumber = models.CharField(max_length=200, null=True, blank=True)
    item = models.ForeignKey(MenuItemsModel, null=True, on_delete=models.CASCADE,
                              blank=True, default=None, related_name='menu_item')
    item_ingredients = models.ManyToManyField(
        ItemIngredientsModel, blank=True, default=None, related_name='item_ingredients')
    sold_price = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.orderNumber

# Create your models here.
class CartModel(models.Model):
    currentUser = models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(CustomerModel, null=True, on_delete=models.CASCADE,
                              blank=True, default=None, related_name='customer_details')
    orderNumber = models.CharField(max_length=200, null=True, blank=True)
    sub_total = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    delivery_fee = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True,default='in_cart')
    items = models.ManyToManyField(
        CartItemsModel, blank=True, default=None, related_name='cart_items')
    notes = models.TextField(blank=True)
    payment_status = models.CharField(max_length=200, null=True, blank=True)
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.orderNumber