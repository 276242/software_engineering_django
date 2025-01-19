from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def validate_positive_price(self):
        if self.price <= 0:
            raise ValidationError('The price must be a positive value.')

    def clean(self):
        self.validate_positive_price()

    def save(self, *args, **kwargs):
        self.validate_positive_price()
        super().save(*args, **kwargs)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Process', 'In Process'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    products = models.ManyToManyField(Product)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def calculate_total_price(self):
        total_price = sum(product.price for product in self.products.all())
        return total_price

    def check_order_fulfillment(self):
        for product in self.products.all():
            if not product.available:
                return False
        return True

    def clean(self):
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError(
                f"Invalid status value: '{self.status}'. Allowed values are: {', '.join(dict(self.STATUS_CHOICES).keys())}")
