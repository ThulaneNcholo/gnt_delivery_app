from django.db import models

# Create your models here.
class CustomerModel(models.Model):
    customer = models.CharField(max_length=200, null=True, blank=True)
    firstName = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    suburb = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.street
