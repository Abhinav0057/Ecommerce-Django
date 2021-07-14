from django.db import models
from store.models import Product, productVariation
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    itemVariation = models.ManyToManyField(productVariation, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField()

    def subtotal(self):
        return self.quantity*self.product.price

    def __str__(self):
        return self.product.product_name
